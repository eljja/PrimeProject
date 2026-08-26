# Proof-or-Counterexample Program

Date: 2026-07-04

This document records the next PrimeProject research posture for the four open problems. A proof attempt is not limited to proving the conjecture directly. It can also:

1. find a direct counterexample;
2. prove the contrapositive;
3. prove that no counterexample can exist;
4. falsify weak proof routes before they waste formalization time.

한국어 요약: 증명은 정면 증명만이 아니다. 반례 하나를 찾으면 추측은 끝나고, 대우법으로 반례가 불가능함을 보이면 증명이 된다. 그래서 PrimeProject는 이제 "증명 후보를 만들고 바로 반례로 부수는" 방식으로 네 난제에 접근한다.

## Executable Artifact

The current executable lab is:

```text
scripts/proof_or_counterexample_lab.py
```

It writes:

```text
data/open-problem/proof-or-counterexample-lab.json
data/open-problem/riemann/rh-ticket-16-proof-or-counterexample.json
data/open-problem/collatz/co-ticket-16-proof-or-counterexample.json
data/open-problem/goldbach/gb-ticket-16-proof-or-counterexample.json
data/open-problem/twin-prime/tp-ticket-16-proof-or-counterexample.json
```

Current status:

```text
attempted_no_full_resolution
```

This is deliberate. A bounded computation can find a counterexample, but a bounded computation cannot prove these universal or infinitude statements by itself.

## 2026-08-13 TICKET-222 Lossless Coupling and Biased-Parity Corrections

TICKET-222 keeps all four parent conjectures at `open_not_proven` and proves
four exact, narrower theorems:

1. the full two-sided dyadic Laplace-band profile uniquely determines every
   finite signed measure compactly supported away from zero;
2. `(h,S,B)` losslessly reconstructs a finite positive Collatz valuation word,
   and the exact cycle question reduces to `2^S-3^h>0` and divisibility by that
   denominator;
3. ordered Goldbach-count parity equals the diagonal prime indicator, which
   proves that parity alone cannot distinguish an exception from a positive
   even count;
4. actual finite-wheel parity variables are biased and obey an exact CRT
   product-correlation formula, so balanced Boolean orthogonality does not
   transfer literally.

These results recover information or close weak routes. They do not control the
unbounded zeta tail, exclude all Collatz codes and divergent rays, prove a
cofinal Goldbach lower bound, or establish a shifted von Mangoldt Type II lower
bound. The machine parent-conjecture resolution count remains zero.

English report: [TICKET-222](lossless-coupling-biased-parity.md).
한국어 보고서: [TICKET-222](lossless-coupling-biased-parity.ko.md).

## Preserved: 2026-08-15 TICKET-221 Sharp Obstruction Certificates

TICKET-221 keeps all four parent conjectures at `open_not_proven` and proves
four exact obstruction or sharpness theorems:

1. every arithmetic-free coordinatewise envelope for the RH dyadic kernel has
   sharp per-scale lower bound `1/4`, hence cannot be summable;
2. the ordered Collatz affine intercept is not determined by `(h,S)` or its
   scalar Baker form, as cyclically inequivalent primitive multi-run witnesses
   with fixed point `133/943` and `995/943` demonstrate;
3. the strict Goldbach `L^p` positivity radius is exactly the minimum model
   coordinate, and any finite certified prefix admits a zero-coordinate
   extension that preserves all old data;
4. full parity on the balanced Boolean cube is orthogonal to every proper
   Walsh monomial, so the stated low-degree Twin stress route cannot detect it.

These theorems do not show that the actual zeta defect, Collatz dynamics,
Goldbach representation function, or Twin von Mangoldt correlation realizes
the abstract obstruction model in the decisive direction. They instead rule
out four insufficient next-lemma formulations. The machine parent-conjecture
resolution count remains zero.

English report: [TICKET-221](sharp-obstruction-certificates.md).
한국어 보고서: [TICKET-221](sharp-obstruction-certificates.ko.md).

## Preserved: 2026-08-14 TICKET-220 Dyadic Partition, Primitive-Word Closure, Refinement Stability, and a Finite-Wheel CRT No-Go

TICKET-220 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. the complete dyadic Laplace-band sum equals total RH-defect multiplicity,
   while one remote atom refutes every finite-window sufficiency claim;
2. the complete TICKET-219 single-mountain Collatz exclusion extends to every
   cyclic rotation and positive power of each primitive root;
3. an exact Minkowski bridge transfers a Goldbach cross-fit certificate under
   fold refinement, and all 140 finite nested bridges pass with outward-rounded
   rational eighth-root bounds;
4. CRT constructs an infinite progression of composite pairs inside every
   fixed admissible twin-wheel class.

The actual-zeta summable dyadic envelope, primitive multi-run Collatz Baker
separation and divergence control, representation-free cofinal Goldbach
refinement margin, and parity-sensitive Twin lower bound beyond every fixed
wheel are not proved. The machine parent-conjecture resolution count remains
zero.

English report: [TICKET-220](dyadic-partition-primitive-refinement-crt.md).
한국어 보고서: [TICKET-220](dyadic-partition-primitive-refinement-crt.ko.md).

## Preserved: 2026-08-13 TICKET-219 Band-pass Defects, Matveev Closure, Cross-fitted Moments, and Qualitative Abel Growth

TICKET-219 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. a positive Laplace-difference kernel gives an exact dyadic RH defect count
   certificate, while the cofinal actual-defect premise is explicitly
   identified as RH-equivalent;
2. an exact rational-interval Matveev threshold at `p=27,456,680,737` meets the
   49-convergent TICKET-218 prefix without a gap and excludes every positive
   single-mountain Collatz cycle;
3. disjoint two-fold model fitting removes same-coordinate leakage and all ten
   finite Goldbach holdout folds pass the exact eighth-moment support test;
4. Twin infinitude is equivalent to unboundedness of the actual Abel transform,
   while an infinite sparse support proves that a positive normalized density-
   scale coefficient is not necessary for abstract infinitude.

The prime-side RH band-pass enclosure, all-word Collatz Baker separation and
divergence control, cofinal Goldbach cross-fitted eighth moment, and actual
parity-corrected Twin Abel unboundedness are not proved. The machine parent-
conjecture resolution count remains zero.

English report: [TICKET-219](bandpass-matveev-crossfit-qualitative-abel.md).
한국어 보고서: [TICKET-219](bandpass-matveev-crossfit-qualitative-abel.ko.md).

## Preserved: 2026-08-13 TICKET-218 Adaptive Radii, Exponential Spikes, Residual Moments, and Abel Surplus

TICKET-218 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial, reduction, or no-go results:

1. the moving radius `r_H=exp(-tau/H)` preserves the first RH defect signal at
   scale `exp(-tau)`, while faster radial approach makes that signal vanish;
2. a single-mountain Collatz candidate that escapes the inherited scaling test
   forces an exponential next continued-fraction denominator spike, and exact
   rational arithmetic excludes the first 49 upper convergents;
3. `sum |A_i-M_i|^p < min_i M_i^p` is a sharp sufficient condition for full
   support, and its exact integer eighth-moment form certifies five finite
   Goldbach blocks where the fourth-moment form fails;
4. `T(Y)>=F(r)-R(r,Y)` transfers a strict Abel surplus to a Twin count lower
   bound, so an actual liminf coefficient above `exp(-a)/2` at horizon
   `(2 log log X+a)X` would imply infinitely many twins.

The actual-zeta adaptive-radius bound, an all-convergent Collatz denominator
bound plus multi-run/divergence control, a cofinal Goldbach eighth-moment
estimate, and the actual Twin Abel coefficient above `1/2` are not proved. The
machine resolution count remains zero.

English report: [TICKET-218](adaptive-radius-spike-residual-surplus.md).
한국어 보고서: [TICKET-218](adaptive-radius-spike-residual-surplus.ko.md).

## Preserved: 2026-08-13 TICKET-217 Relative Thresholds, Convergent Compression, Moment Support, and Critical Abel Tails

TICKET-217 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial, reduction, or no-go results:

1. finitely many RH defect transforms give the exact normalized certificate
   `C(H)<=floor(min_j U_j/r_j^H)`, while fixed absolute errors hide late atoms;
2. every single-mountain Collatz candidate reduces to an upper continued-
   fraction convergent and exact arithmetic excludes `k<71,356,888`;
3. `S^2>(B-1)Q` is a sharp weighted second-moment sufficient condition for
   every Goldbach target in a block to have a representation;
4. at dilation `2 log log X+a`, the coefficient-one Twin Abel tail divided by
   `X/log^2 X` tends exactly to `exp(-a)/2`.

No actual-zeta cofinal relative enclosure, all-convergent and multi-run Collatz
barrier, pointwise Goldbach lower-tail bound, or Twin Abel surplus above the
critical tail is proved. The machine resolution count remains zero.

English report: [TICKET-217](relative-threshold-convergent-moment-tail.md).
한국어 보고서: [TICKET-217](relative-threshold-convergent-moment-tail.ko.md).

## Preserved: 2026-08-13 TICKET-216 Laplace Defects, Cross-Power GCDs, Radix Histograms, and Tauberian Tails

TICKET-216 is the direct input to TICKET-217. Its first-atom RH transform
certificate, Collatz cross-power gcd necessity, exact Goldbach radix histogram,
and quantitative Twin Abel-to-count bracket remain valid within their stated
scopes.

English report: [TICKET-216](laplace-gcd-radix-tauberian.md).
한국어 보고서: [TICKET-216](laplace-gcd-radix-tauberian.ko.md).

## Preserved: 2026-08-12 TICKET-215 Lattice Certificates, Power Near-Collisions, Exception Counts, and Abel Boundaries

TICKET-215 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial, reduction, or no-go results:

1. the nonnegative-even RH defect can be certified by a rigorous interval
   whose upper endpoint is below two; width alone is refuted by `[2,2]`;
2. every Collatz word cyclically equal to `1^k2^m` forces one power
   near-collision per `k`, and exact arithmetic excludes it through `k=4096`;
3. for `Bq<1`, the floor of the exponential Goldbach selector equals the exact
   number of exceptions, and the threshold is universally sharp;
4. the exact gap-two Abel transform diverges at radius one exactly when twins
   are infinite, while any finite radius sample is logically insufficient.

No actual-zeta cofinal upper bound, all-`k` near-collision exclusion,
all-block Goldbach selector bound, or parity-breaking Twin Abel lower bound is
proved. The machine resolution count remains zero.

English report: [TICKET-215](lattice-nearcollision-exception-abel.md).
한국어 보고서: [TICKET-215](lattice-nearcollision-exception-abel.ko.md).

## Preserved: 2026-08-12 TICKET-214 Cofinal Defects, Seven-One Cycles, Exponential Witnesses, and Cardinal Gap Selection

TICKET-214 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. exact multiplicity equality on one unbounded sequence of boundary-free
   heights is RH-equivalent, while critical-line density one and relative
   defect `o(N)` are insufficient;
2. the product bound reduces exactly-seven-one accelerated Collatz cycles to
   lengths `8..26`, and exact enumeration excludes all `4,349,349` candidates;
3. the scale-growing exponential sum `sum 2^(-k_B A_i)` is below one exactly
   when a finite Goldbach block has no exception, while the sharp occupancy
   bound shows total witness mass and a cap do not prevent concentration;
4. cardinal-sine interpolation selects gap two exactly on every even integer
   gap, while unboundedness of that exact functional remains equivalent to
   twin-prime infinitude.

No actual-zeta cofinal equality, uniform Collatz all-stratum divisor witness,
uniform Goldbach selector bound, or unbounded Twin arithmetic minorant is
proved. The machine resolution count remains zero.

English report: [TICKET-214](cofinal-sevenone-exponential-cardinal.md).
한국어 보고서: [TICKET-214](cofinal-sevenone-exponential-cardinal.ko.md).

## Preserved: 2026-08-12 TICKET-213 Multiplicity, Six-One Cycles, Polynomial Majorants, and Gap Selectors

TICKET-213 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. total critical-line multiplicity `M` gives the exact finite-rectangle RH
   certificate `N-M<2`, while odd-multiplicity sign counts also demand zero
   simplicity and therefore define a strictly stronger target;
2. the product bound reduces exactly-six-one accelerated Collatz cycles to
   lengths `7..22`, and exact enumeration excludes all `376,788` candidates;
3. unbounded attained Goldbach representation multiplicity rules out every
   fixed polynomial pointwise exception majorant, and exact interpolation on
   witness counts through `M` requires degree at least `M`;
4. a nonnegative weighted gap functional selects gap two on the whole
   nonnegative cone exactly when its positive support is only gap two.

The all-height zeta multiplicity equality, Collatz strata with seven or more
ones and nonperiodic divergence, a scale-growing Goldbach resummation below
one, and a signed arithmetic gap-two selector with a uniform remainder are not
proved. The machine resolution count remains zero.

English report: [TICKET-213](multiplicity-sixone-polynomial-selector.md).
한국어 보고서: [TICKET-213](multiplicity-sixone-polynomial-selector.ko.md).

## Preserved: 2026-08-12 TICKET-212 Even Defect, 2-Adic Ghosts, Full-Witness Products, and Gap Channels

TICKET-212 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. in a symmetric upper critical-strip rectangle, total zero count `N` and
   `L` certified Hardy sign-change intervals satisfy a sharp sufficient
   condition: `N-L<2` forces every zero to be simple and on the critical line;
2. every accelerated Collatz valuation word has a unique `2`-adic ghost
   cycle, so `Z_2` membership cannot be an exclusion theorem and the correct
   ordinary-integer target is `(2^A-3^h)|C` with positive divisor;
3. the full Goldbach exception indicator is the exact product of witness
   failures, while every fixed even-order Bonferroni upper bound equals
   `binomial(A-1,2r)` on represented targets; a prime-pair pigeonhole count
   and the prime number theorem make `A` unbounded, so a fixed order fails on
   arbitrarily large targets;
4. Twin Prime is equivalent to gap-two positivity on infinitely many dyadic
   blocks, while positive mass summed over finitely many bounded-gap channels
   does not identify the gap-two channel.

The all-height RH defect bound, uniform Collatz odd-divisor nondivisibility,
uniform Goldbach witness-product resummation below one, and infinitely-often
gap-two channel positivity are not proved. The machine resolution count
remains zero.

English report: [TICKET-212](even-defect-ghost-bonferroni-gapchannel.md).
한국어 보고서: [TICKET-212](even-defect-ghost-bonferroni-gapchannel.ko.md).

## Preserved: 2026-08-10 TICKET-211 Winding Localization, Collatz Integrality, Full-Range Goldbach Exceptions, and Unit-Scale Twin Deserts

TICKET-211 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate or no-go results:

1. functional symmetry, effective cofinal horizontal clearance, and exact
   total winding do not imply critical-line zero localization;
2. every positive accelerated Collatz cycle must satisfy
   `k/h>=log_2(6/5)`, while an exact rational family shows that aggregate
   density, contraction, and product identities do not enforce integrality;
3. a small-witness Goldbach exception count cannot be the integer count driven
   below one, so the target is corrected to full-range nonrepresentation;
4. factorial twin deserts reach every fixed coefficient `c<1` of
   `log X/log log X`.

Critical-line rectangle zero-count equality, a uniform 2-adic Collatz
integrality obstruction, a full-range Goldbach exceptional count below one,
and sparse dyadic Twin positivity are not proved. The machine resolution count
remains zero.

English report: [TICKET-211](winding-density-fullrange-unitscale.md).
한국어 보고서: [TICKET-211](winding-density-fullrange-unitscale.ko.md).

## Preserved: 2026-08-10 TICKET-210 Cofinal Lines, Five-One Cycles, Prime-Gap Transfer, and Scaled Twin Deserts

TICKET-210 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. existential cofinal central zeta nonvanishing holds, but an exact symmetric
   off-critical countermodel shows that it does not imply RH;
2. no nontrivial positive accelerated Collatz cycle has exactly five
   valuation-one entries and arbitrary remaining valuations at least two;
3. consecutive prime gaps transfer exactly to least Goldbach witness lower
   bounds, but the current published gap theorem is weaker than TICKET-209's
   covering-congruence floor;
4. factorial twin deserts have length at least
   `(1/4) log X/log log X`, ruling out every-window positivity at that scale.

Effective Riemann winding, a multiplicity-uniform Collatz obstruction,
Goldbach exceptional-tail control below one, and a dyadic Twin phase lower
bound permitting local deserts are not proved. The machine resolution count
remains zero.

English report: [TICKET-210](cofinal-fiveone-primegap-scaledtwin.md).
한국어 보고서: [TICKET-210](cofinal-fiveone-primegap-scaledtwin.ko.md).

## Preserved: 2026-08-10 TICKET-209 Normalized Boundaries, Four-One Cycles, Covering Congruences, and Factorial Twin Deserts

TICKET-209 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. a height-independent positive absolute completed-xi margin on cofinal full
   boundaries is impossible; gamma normalization leaves a central-edge task;
2. no nontrivial positive accelerated Collatz cycle has exactly four
   valuation-one entries;
3. an unbounded even sequence has least Goldbach witness above
   `c log N log log N` for an absolute `c>0`, without producing a Goldbach
   counterexample;
4. arbitrarily long factorial twin-free intervals have exact cyclotomic
   remainder `R_I=-H`, refuting every-interval positive phase margins.

Gamma-normalized central-edge nonvanishing, five-one Collatz necklaces,
Goldbach tail exceptional control beyond the covering floor, and an independent
dyadic Twin phase lower bound are not proved. The machine resolution count
remains zero.

English report: [TICKET-209](normalized-fourone-covering-factorial.md).
한국어 보고서: [TICKET-209](normalized-fourone-covering-factorial.ko.md).

## Preserved: 2026-08-10 TICKET-208 Vertical Clearance, Three-One Cycles, Unit-Log Witnesses, and Cyclotomic Correlations

TICKET-208 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. both completed-xi vertical sides have an explicit positive lower bound at
   every finite height, while vertical nonvanishing alone cannot locate all
   interior zeros;
2. no nontrivial positive accelerated Collatz cycle has exactly three
   valuation-one entries;
3. for every fixed `c < 1`, an unbounded sequence has least Goldbach witness
   above `c log N`, without producing a Goldbach counterexample;
4. a growing cyclotomic Omega projector exactly reconstructs finite interval
   twin counts, while twin-free intervals exhibit exact zero-mode cancellation.

The completed-xi cofinal top-edge clearance, four-one Collatz necklaces,
Goldbach tail exceptional estimate below one beyond the unit-log floor, and
strict cofinal Twin nonzero-mode remainder bound are not proved. The machine
resolution count remains zero.

English report: [TICKET-208](vertical-threeone-unitlog-cyclotomic.md).
한국어 보고서: [TICKET-208](vertical-threeone-unitlog-cyclotomic.ko.md).

## Preserved: 2026-08-10 TICKET-207 Dihedral Boundaries, Two-One Cycles, Logarithmic Witnesses, and Abel Leakage

TICKET-207 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. completed-xi rectangle certification reduces to the top edge and upper
   right half-edge, while the same symmetries alone do not force critical-line
   zeros;
2. no nontrivial positive accelerated Collatz cycle has exactly two valuation-
   one entries and arbitrary remaining valuations at least two;
3. an unbounded CRT sequence has least Goldbach witnesses above
   `(1/3) log N`, without producing a Goldbach counterexample;
4. the Abel-Omega projector has a closed form and exactly reconstructs finite
   twin counts after flooring, but supplies no independent positivity.

The completed-xi cofinal interval bounds, remaining Collatz necklaces,
Goldbach tail exceptional estimate below one, and signed Twin main term are not
proved. The machine resolution count remains zero.

English report: [TICKET-207](dihedral-twoone-logwitness-abel.md).
한국어 보고서: [TICKET-207](dihedral-twoone-logwitness-abel.ko.md).

## Preserved: 2026-08-10 TICKET-206 Adaptive Certificates, Single-One Cycles, CRT Witnesses, and Omega Projectors

TICKET-206 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. positive boundary clearance implies finite termination of the derivative-
   certified winding mesh, while fixed budgets fail at inverse-clearance scale;
2. no nontrivial positive accelerated Collatz cycle has exactly one valuation
   one and arbitrary remaining valuations at least two;
3. every fixed bound on Goldbach prime witnesses is defeated by an infinite CRT
   progression, without producing a Goldbach counterexample;
4. Omega-binomial inversion is an exact prime projector, but every finite
   truncation has infinitely many positive composite-composite shift-two false
   positives.

The completed-zeta interval bounds, remaining mixed Collatz necklaces,
growing-cutoff Goldbach tail estimate, and uniform Twin projector-tail
cancellation are not proved. The machine resolution count remains zero.

English report: [TICKET-206](adaptive-singleone-crt-projector.md).
한국어 보고서: [TICKET-206](adaptive-singleone-crt-projector.ko.md).

## Preserved: 2026-08-10 TICKET-205 Winding Certificates, Cycle Extrema, Finite Witnesses, and Omega Weights

TICKET-205 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial, finite, or no-go results:

1. segmentwise derivative bounds make the sampled polygon winding equal the
   analytic contour winding, while finite contour values alone do not;
2. a nontrivial positive Collatz cycle has valuation 1 at a minimum and at
   least 2 at a maximum, eliminating the complete all-valuations-at-least-two
   periodic stratum except the fixed cycle 1;
3. every even target through 10,000,000 has an exact least-prime Goldbach
   witness, with a stable SHA-256 for the complete witness stream;
4. `W(n)=2-(3/2)Omega(n)` realizes the desired prime/semiprime signs, but an
   infinite CRT family proves that positive raw shift-two products do not
   isolate twin primes.

The RH regression is not Xi, the Collatz theorem does not address mixed words
or divergent trajectories, the Goldbach result is finite, and the Twin weight
has no uniform composite-cancellation theorem. The machine resolution count
remains zero.

English report: [TICKET-205](winding-extremal-finite-omega.md).
한국어 보고서: [TICKET-205](winding-extremal-finite-omega.ko.md).

## Preserved: 2026-08-10 TICKET-204 Continuous Certificates, Primitive Necklaces, and Parity Kernels

TICKET-204 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. sampled relative contour error, a covering radius, and an arclength
   derivative bound imply a continuous Rouché bound, while finite samples
   without regularity do not;
2. Collatz affine cycle integrality is invariant under cyclic rotation and word
   powers, so periodic candidates reduce to primitive necklaces;
3. after finite verification, a Goldbach tail exceptional-count bound strictly
   below one closes the universal quantifier, whereas density zero and a bound
   at most one do not;
4. a PSD kernel cannot be negative on every semiprime factor channel, while a
   formal indefinite rank-two kernel separates exposed factor channels.

The RH fixtures are not Xi, the Collatz enumeration is finite, the Goldbach
countermodels are not prime arithmetic, and the Twin escape is not yet an
arithmetic sieve weight. The machine resolution count remains zero.

English report: [TICKET-204](mesh-necklace-exceptional-kernel.md).
한국어 보고서: [TICKET-204](mesh-necklace-exceptional-kernel.ko.md).

## Preserved: 2026-08-10 TICKET-203 Rouché Transfer, Signed Valuation Transfer, and Pointwise Target Correction

TICKET-203 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial or no-go results:

1. a strict Rouché margin, comparison zero count, and independently included
   zero list of the same multiplicity imply exact zero exhaustion;
2. a signed two-site Collatz valuation transfer changes the affine numerator
   by an exact prefix-segment formula, while `(3,1)->(2,2)` refutes universal
   nondivisibility preservation;
3. pointwise Goldbach defect positivity is exactly equivalent to a
   prime-prime representation on a Chen-positive channel, while a fixed
   `c/log log N` lower bound is quantitatively stronger;
4. fixed primorial single-coordinate data cannot separate every prime from
   every rough semiprime, while scale-growing bilinear switching remains open.

The RH theorem supplies no actual Xi margin. The Collatz counterexample reaches
the known trivial fixed cycle. The Goldbach countermodel is abstract integer
channel data. The Twin theorem has a deliberately fixed-local scope. The
machine resolution count remains zero.

English report: [TICKET-203](rouche-transfer-pointwise-primorial.md).
한국어 보고서: [TICKET-203](rouche-transfer-pointwise-primorial.ko.md).

## Preserved: 2026-08-10 TICKET-202 Exact Hermite Data, Long-Run Deformations, and Parity Scale

TICKET-202 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial results:

1. finitely many exact symmetric Hermite constraints, even with compact
   finite-jet control, cannot force a global real-zero property in the ambient
   real-even entire-function class;
2. every `r,k>=2`, `t>=0`, and cyclic rotation in the primitive Collatz family
   `1^k2^(2k+t)(12^2)^(r-1)` fails affine divisibility;
3. the dyadic aggregate Goldbach P2 relative Liouville defect is
   `O(1/log log X)` and tends to zero, so a fixed positive pointwise defect on
   every large input is impossible;
4. a fixed Twin relative defect plus Chen-order channel mass implies a
   Hardy-Littlewood-order quantitative pair lower bound and is stronger than
   mere infinitude at the channel-algebra level.

The RH perturbation changes the function and is not an Xi counterexample. The
Collatz theorem covers one one-sided deformation family, not arbitrary words.
The Goldbach result is aggregate rather than pointwise. The Twin countermodel
is abstract channel data rather than prime arithmetic. The machine resolution
count remains zero.

English report: [TICKET-202](exact-hermite-deformation-parity-scale.md).
한국어 보고서: [TICKET-202](exact-hermite-deformation-parity-scale.ko.md).

## 2026-08-10 TICKET-201 Finite Information, All-Run Collatz, and Liouville Parity

TICKET-201 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial results:

1. fixed compact finite-order jet data cannot force a global real-zero
   property in the ambient real-even entire-function class;
2. every `r,k>=2` and cyclic rotation in the Collatz family
   `1^k2^(2k)(12^2)^(r-1)` fails affine divisibility by one exact identity;
3. `R=(C-L)/2` exactly projects the Goldbach prime channel inside P2 support,
   proving that the previous semiprime-elimination target was
   conjecture-equivalent on Chen-positive inputs;
4. `T=(C2-L2)/2` exactly projects the Twin channel in dyadic blocks, proving
   that the previous infinitely-many-positive-block target was the Twin Prime
   conjecture in dyadic language.

The finite rows check implementation consistency only. No global Liouville
defect, cofinal Xi certificate, arbitrary Collatz-word obstruction, or
conjecture resolution is claimed. The machine resolution count remains zero.

English report: [TICKET-201](finite-information-allrun-liouville-parity.md).
한국어 보고서: [TICKET-201](finite-information-allrun-liouville-parity.ko.md).

## 2026-08-10 TICKET-200 Derivative Meshes, Three-Run Obstruction, and Chen Channels

TICKET-200 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results:

1. a sampled boundary margin propagates over the complete `D3+` boundary when
   paired with a certified derivative budget satisfying `eta-Lh/2>0`; the
   exact regression instance is synthetic and no Xi enclosure is claimed;
2. the primitive Collatz family `1^k2^(2k)(12^2)^2` is excluded at every
   scale `k>=2` and every cyclic rotation by exact affine formulas;
3. Bordignon's explicit Chen theorem decomposes exactly into Goldbach's
   prime-prime and prime-composite-semiprime channels, so a possible large
   Goldbach counterexample must be semiprime-only;
4. Chen's infinitely many prime-plus-`P2` starts decompose into twin and
   composite-semiprime channels, exposing the exact fixed-shift parity gap.

The two Chen theorems are imported and are not reproved. Finite channel counts
are regression checks, not universal or infinitely-often proofs. The machine
resolution count remains zero.

English report: [TICKET-200](derivative-mesh-three-run-chen-channels.md).
한국어 보고서: [TICKET-200](derivative-mesh-three-run-chen-channels.ko.md).

## 2026-08-10 TICKET-199 Symmetric Sampling, Two-Run Obstruction, and Squarefree-Lambda Filters

TICKET-199 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results:

1. finite boundary point samples admit exact real-even polynomial
   countermodels, so an RH Rouché certificate must control every boundary
   interval or a derivative envelope;
2. the primitive Collatz family `1^k2^(2k)12^2` is excluded at every scale
   `k>=2` and every cyclic rotation by an exact affine-divisibility obstruction;
3. `P=mu^2 Lambda` is an exact prime projector and turns Goldbach into exact
   positivity of `P*P`, without proving the required pointwise lower bound;
4. the localized shift-two `P` correlation exactly detects twin pairs, without
   proving infinitely many positive blocks.

The finite computations are regression checks for exact arguments. They do not
promote finite positivity to a universal or infinitely-often theorem. The
projector identity is elementary and no literature-priority claim is made.

English report: [TICKET-199](symmetric-sampling-two-run-squarefree-filter.md).
한국어 보고서: [TICKET-199](symmetric-sampling-two-run-squarefree-filter.ko.md).

## 2026-08-09 TICKET-198 Verified Height, Primitive Words, and Quantifier Strength

TICKET-198 keeps all four parent conjectures at `open_not_proven` and proves
four exact statements:

1. the peer-reviewed finite-height RH theorem through `3*10^12` transfers to
   `2,999,999,999,999` integer Xi rectangle levels, existentially but without
   an explicit Taylor degree or control above that height;
2. using TICKET-183 primitive reduction as an input, every fixed Collatz run
   count `r>=2` still contains the infinite primitive family
   `1^k2^(2k)(12^2)^(r-1)` passing both scalar gates;
3. collision-free Goldbach positivity alone yields only an
   `O(X/log^2 X)` exceptional-set bound, and a surrogate supported on
   `{2p^2}` refutes only the promotion rule, not Goldbach;
4. a Twin block-mass lower bound at scale `sqrt(X)log(X)` forces an unbounded
   square-root-scale pair count, exposing the previous target as overstrong.

The revised next lemmas are a standalone interval Taylor/Rouché certificate on
`D3`, a uniform all-length affine obstruction for primitive fixed-run words, a
pointwise margin on the Goldbach collision-supported stratum, and a localized
prime-power-free Twin detector positive on infinitely many blocks.

English report: [TICKET-198](verified-height-primitive-word-quantifier-strength.md).
한국어 보고서: [TICKET-198](verified-height-primitive-word-quantifier-strength.ko.md).

## 2026-08-08 TICKET-197 First Rectangle, Run Blocks, and Sparse Collisions

TICKET-197 keeps all four parent conjectures at `open_not_proven` and proves
four exact partial theorems.

1. **Riemann:** `ActualXiFirstRectangleExistenceAndVacuityBoundary` proves
   existential Taylor-Rouché closure of the actual-Xi `D_2` rectangles and
   simultaneously proves that those rectangles avoid the open critical strip.
   No explicit degree or interval margin is produced.
2. **Collatz:** `ContiguousOneTwoRunAffineDivisibilityObstruction` excludes
   `1^k2^(2k)` and every cyclic rotation for all `k>=1`, even though the family
   passes both scalar gates. Arbitrary alternating runs remain open.
3. **Goldbach:** `GoldbachPrimePowerCollisionSupportHasDensityZero` proves
   that the target support of `Q*Q` has size `O(X/log^2 X)=o(X)`. The overlap
   correction is exact but cannot supply a uniform every-even margin.
4. **Twin Prime:** `TwinPrimeEqualExponentCollisionNoGoAndLowerOrderSaving`
   proves equal-exponent gap-two prime-power collisions impossible and bounds
   the weighted overlap by `O(X^(1/3)log X)`. The leading square layer and
   parity barrier remain.

Machine audit: four exact theorems, 2 exact Xi coordinate rows, 64 exact
Collatz scales, 17 Goldbach support scales, 21 Twin dyadic scales, zero
conjecture resolutions, and zero failures.

English report: [TICKET-197](first-rectangle-run-block-sparse-collision.md).
한국어 보고서: [TICKET-197](first-rectangle-run-block-sparse-collision.ko.md).

## 2026-08-08 TICKET-196 Rouché Exhaustion, Density No-Go, and Collision Corrections

TICKET-196 keeps all four parent conjectures at `open_not_proven` and proves
four exact route corrections.

1. **Riemann:** `RoucheExhaustionEquivalenceAndIntermediateTargetNoGo` proves
   that zero-free Rouché certificates for Taylor sections on an exhausting
   family of rational off-real rectangles are equivalent to the entire
   function having only real zeros. Applied to Xi, the former next target was
   RH-equivalent rather than a weaker intermediate lemma. The retained next
   target is one certified rectangle for the actual Xi function.
2. **Collatz:** `OneTwoValuationDensityWindowAndScalarGateNoGo` proves that the
   contraction and product gates allow the infinite count-profile family
   `(h,r)=(3k,k)`. These profiles are not cycles; they show that scalar density
   alone cannot replace the missing order-sensitive affine divisibility
   obstruction.
3. **Goldbach:** `CollisionCorrectedGoldbachPrimePowerEnvelope` proves the
   exact odd-support identity `E_o(N)=2(Q*Lambda_o)(N)-(Q*Q)(N)`. The witness
   `18=9+9` demonstrates the strictly positive overlap correction. The
   every-large-even lower bound is still open.
4. **Twin Prime:** `CollisionCorrectedTwinPrimePowerEnvelope` proves the local
   shift-two inclusion-exclusion identity and subtracts
   `sum Q(n)Q(n+2)`. The witness `(25,27)=(5^2,3^3)` demonstrates a positive
   collision correction. A parity-breaking lower bound on infinitely many
   blocks is still open.

Machine audit: four exact theorems, one RH target-equivalence no-go, one
Collatz scalar-density no-go, two collision-corrected envelopes, 11 synthetic
Rouché rows, 64 exact Collatz profiles, two positive overlap witnesses, zero
conjecture resolutions, and zero failures.

English report: [TICKET-196](rouche-density-overlap.md).
한국어 보고서: [TICKET-196](rouche-density-overlap.ko.md).

## 2026-08-08 TICKET-195 Finite-Jet Boundaries, Eleven-One Decidability, and Prime-Square Layers

TICKET-195 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results.

1. **Riemann:** `FiniteEvenJetAmbiguityAndRoucheTailBridge` constructs, for
   every finite real even Taylor jet, an extension with the same declared jet
   and nonreal zeros at `+i` and `-i`. This refutes finite-jet-only promotion.
   Strict Rouché tail control remains a valid bounded-domain bridge, but the
   actual Xi tail margin is not proved.
2. **Collatz:** `FixedOneCountRestTwoDecidabilityAndElevenStratumExclusion`
   proves every fixed one-count/rest-two stratum decidable and closes the
   complete eleven-one stratum. Noncontraction closes `h<=26`, a complete 5+5
   MITM audit represents 3,151,735,808 normalized words at `h=27..41`, and
   `2048(5/6)^h<1` closes `h>=42`.
3. **Goldbach:** `PrimeSquareDominantThetaLayerDecomposition` splits odd
   proper-prime-power mass into the prime-square layer and an `O(N^(1/3))`
   higher-exponent remainder. The identity `32=3^3+5` refutes exact
   square-only support deletion.
4. **Twin Prime:** `PrimeSquareDominantIntervalThetaLayerDecomposition` proves
   the interval analogue with an `O(X^(1/3))` higher-layer remainder. The pair
   `(27,29)` refutes exact square-only gap-two support deletion.

Machine audit: four exact theorems, one finite-jet no-go, one fixed-stratum
decidability theorem, one newly closed infinite Collatz stratum, two
prime-square layer decompositions, 3,151,735,808 represented Collatz words,
zero conjecture resolutions, and zero failures.

English report: [TICKET-195](finitejet-elevenone-squarelayer.md).
한국어 보고서: [TICKET-195](finitejet-elevenone-squarelayer.ko.md).

## 2026-08-08 TICKET-194 Dense-Core Extension, Ten-One Cycles, and Theta Layers

TICKET-194 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results.

1. **Riemann:** `UniformlyBoundedDenseCoreQuadraticConvergenceExtendsEverywhere`
   proves that one uniform operator bound plus convergence on a dense core
   yields a bounded Hermitian limit on the whole Hilbert space. The positive,
   monotone family `q_n(x)=sum_(k<=n) k|x_k|^2` proves that those core
   properties alone do not imply the uniform bound.
2. **Collatz:** `ExactlyTenValuationOnesOtherwiseTwoCycleExclusion` closes the
   complete ten-one/rest-two periodic stratum. Noncontraction closes `h<=24`,
   a complete 5+4 MITM residue audit represents 470,772,500 normalized words at
   `h=25..38`, and `1024(5/6)^h<1` closes `h>=39`.
3. **Goldbach:** `OddPrimePowerThetaLayerCompressionAndBinaryMassClassification`
   proves the exact odd proper-prime-power theta-layer identity and classifies
   the power-of-two pair mass. The classical Chebyshev bound lowers the
   analytical contamination scale to `O(sqrt(N) log N)`.
4. **Twin Prime:** `OddPrimePowerIntervalThetaLayerCompression` proves the exact
   interval theta-layer identity and lowers the shift-two contamination scale
   to `O(sqrt(X) log X)`.

Machine audit: four exact theorems, one newly closed infinite Collatz stratum,
two exact theta-layer identities, 470,772,500 represented Collatz words, four
rejected or corrected routes, zero conjecture resolutions, and zero failures.

English report: [TICKET-194](densecore-tenone-theta-layers.md).
한국어 보고서: [TICKET-194](densecore-tenone-theta-layers.ko.md).

## 2026-08-08 TICKET-193 Everywhere Extension, Nine-One Cycles, and Parity Envelopes

TICKET-193 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results.

1. **Riemann:** `EverywherePointwiseQuadraticConvergenceForcesUniformBoundedExtension`
   proves that pointwise convergence on every vector of a complete Hilbert
   space forces uniform operator boundedness and a bounded Hermitian limit.
   The spike family `q_n(x)=n|x_n|^2` refutes dense-core-only promotion.
2. **Collatz:** `ExactlyNineValuationOnesOtherwiseTwoCycleExclusion` closes the
   complete nine-one/rest-two periodic stratum. Noncontraction closes `h<=21`,
   a complete 4+4 MITM residue audit represents 52,157,326 normalized words at
   `h=22..34`, and `512(5/6)^h<1` closes `h>=35`.
3. **Goldbach:** `ParitySeparatedPrimePowerContaminationEnvelope` proves
   `E_pp(N)<=2log(N)W_odd(N)+C_2(N)` for even `N>=6`, with
   `C_2(N)<=2(log 2)^2` classified exactly.
4. **Twin Prime:** `OddOnlyShiftTwoContaminationEnvelope` proves that every
   von Mangoldt-supported shift-two pair in `[X,2X)`, `X>=4`, is odd and hence
   only odd local proper-prime-power mass needs to be charged.

Machine audit: four exact theorems, one newly closed infinite Collatz stratum,
two parity-sharpened envelopes, 52,157,326 represented Collatz words, four
rejected or corrected routes, zero conjecture resolutions, and zero failures.

English report: [TICKET-193](everywhere-nineone-parity-envelope.md).
한국어 보고서: [TICKET-193](everywhere-nineone-parity-envelope.ko.md).

## 2026-08-08 TICKET-192 Uniform Extension, Eight-One Cycles, and Weighted Envelopes

TICKET-192 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results.

1. **Riemann:** `UniformBoundedCoreExtensionAndPointwiseCauchyNoGo` proves that
   a dense-core Hermitian quadratic form extends boundedly exactly when it has
   one uniform quadratic norm bound. Positive pointwise-Cauchy sections with
   norms tending to infinity refute pointwise-only promotion.
2. **Collatz:** `ExactlyEightValuationOnesOtherwiseTwoCycleExclusion` closes
   the complete eight-one/rest-two periodic stratum. Noncontraction closes
   `h<20`, rotation-normalized exact arithmetic closes 5,777,343 words at
   `h=20..30`, and `256(5/6)^h<1` closes `h>=31`.
3. **Goldbach:** `WeightedPrimePowerEnvelopeAndFactorTwoBudgetReduction`
   proves `E_pp(N)<=2log(N)W_pp(N)<=A(N)(log N)^2`, removing the earlier
   count-budget factor two. The every-large-even correlation lower bound is open.
4. **Twin Prime:** `LocalTwoSidedWeightedEnvelopeBridge` bounds contamination
   by the weighted proper-power mass in the two translated local intervals.
   Finite blocks pass; infinitely many unbounded successful blocks are open.

Machine audit: four exact theorems, one newly closed infinite Collatz stratum,
two weighted-envelope bridges, four rejected or corrected routes, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-192](uniform-eightone-weighted-envelope.md).
한국어 보고서: [TICKET-192](uniform-eightone-weighted-envelope.ko.md).

## 2026-08-08 TICKET-191 Probe Topology, Seven-One Cycles, and Exact Arithmetic Targets

TICKET-191 keeps all four parent conjectures at `open_not_proven` and proves
four exact intermediate results.

1. **Riemann:** `GaussianRationalProbePromotionAndCoordinateTestNoGo` lowers
   the promotion target to Cauchy convergence of Gaussian-rational finite-support
   probes plus a vanishing negative floor. The matrix `[[1,-a],[-a,1]]`, `a>1`,
   refutes coordinate-only positivity. Actual Weil-probe estimates remain open.
2. **Collatz:** `ExactlySevenValuationOnesOtherwiseTwoCycleExclusion` closes
   the complete seven-one/rest-two periodic stratum. The product bound
   `128(5/6)^h<1` closes `h>=27`; exact arithmetic closes all 2,195,765 words at
   `h=17..26` with zero divisibility hits.
3. **Goldbach:** `ExactPrimePowerBudgetPointwiseReductionAndLinearScaleNoGo`
   proves that pointwise excess above the explicit proper-prime-power budget is
   sufficient and that the budget is `o(N)`. The required every-target excess
   remains unproved.
4. **Twin Prime:** `ArithmeticBlockGranularityEquivalenceAndLinearDensityNoGo`
   proves exact equivalence between positive prime-power-subtracted block excess
   and a twin pair in that block. Linear density is not necessary; positivity
   on infinitely many actual blocks remains open.

Machine audit: four exact theorems, one newly closed infinite Collatz stratum,
three sharpened quantifier-matched targets, four rejected or corrected routes,
zero conjecture resolutions, and zero computational failures.

English report: [TICKET-191](probe-sevenone-budget-granularity.md).
한국어 보고서: [TICKET-191](probe-sevenone-budget-granularity.ko.md).

## 2026-08-08 TICKET-190 Cauchy Cores, Six-One Cycles, and Quantifier Transfer

TICKET-190 continues from TICKET-189 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `DirectCoreCauchyPromotionAndAbsoluteSummabilityNoGo` proves
   that a direct fixed-core Cauchy modulus suffices for compatible form
   convergence. An alternating harmonic core refutes absolute adjacent-drift
   summability as a necessary condition, while `diag(1,...,m)` separates a
   positive form on `c_00` from a bounded `l_2` operator. The next obligation is
   `PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor`.
2. **Collatz:** `ExactlySixValuationOnesOtherwiseTwoCycleExclusion` closes
   every contracting word with exactly six valuation-one entries and all
   remaining entries two. The cycle product bound `64(5/6)^h<1` closes
   `h>=23`; exact enumeration closes all 238,722 words at `h=15..22`. The next
   obligation is
   `NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `DensityOneAndAverageMassDoNotImplyEveryTargetGoldbach`
   constructs a sparse-hole countermodel with zeros at every power of two,
   density-zero exceptions, and only `O(X)` missing mass from a quadratic
   average. The next obligation remains the pointwise every-target theorem
   `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget`.
4. **Twin Prime:** `CumulativeDyadicLinearTransferAndSparseMassNoGo` proves
   the equivalence between positive linear cumulative limsup and positive
   linear mass on infinitely many dyadic blocks. The model `b_j=1` proves that
   this linear target is stronger than infinitude. The next obligation is
   `CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope`.

Machine audit: four exact theorems, one newly closed infinite cycle stratum,
three topology or quantifier boundaries, four rejected or corrected routes,
zero conjecture resolutions, and zero computational failures.

English report: [TICKET-190](cauchy-sixone-quantifier-transfer.md).
한국어 보고서: [TICKET-190](cauchy-sixone-quantifier-transfer.ko.md).

## 2026-08-08 TICKET-189 Summable Cores, Five-One Cycles, and Prime-Power Subtraction

TICKET-189 continues from TICKET-188 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `SummableFiniteCoreDriftConstructsCompatiblePositiveForm`
   proves that a summable adjacent operator-drift majorant on every fixed core
   constructs one compatible Hermitian form, and a vanishing negative floor
   makes that form positive on `c_00`. The harmonic scalar core refutes the
   weaker drift-tends-to-zero route. The next obligation is
   `PoleNeutralGuinandWeilFixedCoreDriftHasCertifiedSummableOperatorMajorantAndVanishingNegativeFloor`.
2. **Collatz:** `ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion` closes
   every contracting word with exactly five valuation-one entries and all
   remaining entries two. An all-word odd-quotient bound closes `h>=22`; exact
   enumeration closes all 72,897 words at `h=13..21`. The next obligation is
   `NoContractingValuationWordWithExactlySixOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `ProperPrimePowerContaminationHasExplicitSublinearBudget`
   proves `A(N)<=sqrt(N)+O(log(N)N^(1/3))` and hence `E_pp(N)=o(N)`. This does
   not lower-bound the full convolution. The next obligation is
   `ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget`.
4. **Twin Prime:** `ShiftTwoVonMangoldtPrimePowerContaminationBridge` proves
   the exact shift-two decomposition and an `o(X)` contamination bound. The
   positive composite term `(25,27)=(5^2,3^3)` rejects positivity without
   subtraction. The next obligation is
   `ShiftTwoVonMangoldtCorrelationHasPositiveLinearLowerBoundOnInfinitelyManyDyadicBlocks`.

Machine audit: four exact theorems, one newly closed infinite cycle stratum,
one shared Goldbach/Twin prime-power bridge, four rejected or corrected routes,
zero conjecture resolutions, and zero computational failures.

English report: [TICKET-189](summable-core-fiveone-sublinear-shift.md).
한국어 보고서: [TICKET-189](summable-core-fiveone-sublinear-shift.ko.md).

## 2026-08-02 TICKET-188 Common Forms, Four-One Cycles, Prime Powers, and Dyadic Oracles

TICKET-188 continues from TICKET-187 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `CommonFormDefectPromotionAndMovingDirectionNoGo` proves that
   exact nested negative defect is nondecreasing and that approximate promotion
   requires certified convergence to one fixed form. The family
   `diag(1,...,1,-1/N)` refutes defect-only reasoning. The next obligation is
   `PoleNeutralGuinandWeilMatricesConvergeToOneCommonFormWithCertifiedVanishingOperatorError`.
2. **Collatz:** `ExactlyFourValuationOnesOtherwiseTwoCycleExclusion` closes
   every contracting word with exactly four valuation-one entries and all
   remaining entries two. A cyclic-gap bound proves `1<B/D<3` for `h>=16`;
   exact enumeration closes all 4,116 words at `h=10..15`. The next obligation
   is `NoContractingValuationWordWithExactlyFiveOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `VonMangoldtPrimePowerContaminationBridge` proves
   `R_Lambda=P_Lambda+E_pp` and `E_pp<=2A(N)(log N)^2`. It rejects identifying
   total von Mangoldt mass with prime-prime mass. The next obligation is
   `ExplicitBinaryGoldbachVonMangoldtLowerBoundDominatesPrimePowerContaminationForEveryLargeEvenTarget`.
4. **Twin Prime:** `SubFourTwinIntervalExactCountOracleAndDyadicEquivalence`
   proves that every sound interval narrower than four recovers the exact
   dyadic twin count and that positive lower endpoints on infinitely many
   dyadic blocks are equivalent to twin infinitude. The next obligation is
   `IndependentTypeIITwinProjectorLowerEndpointIsPositiveOnInfinitelyManyDyadicBlocks`.

Machine audit: four exact theorems, one newly closed infinite cycle stratum,
four rejected or corrected routes, zero conjecture resolutions, and zero
computational failures.

English report: [TICKET-188](nested-fourone-primepower-dyadic.md).
한국어 보고서: [TICKET-188](nested-fourone-primepower-dyadic.ko.md).

## 2026-08-02 TICKET-187 Provenance, Three-One Cycles, Signatures, and Intervals

TICKET-187 continues from TICKET-186 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `PublishedFiniteWeilLDLTProvenanceAndOneSectionNoGo` pins the
   published `c=100,N=200` provenance report containing 401 positive interval-
   LDL pivots and no negative or undetermined pivot. PrimeProject does not
   claim an independent 9000-bit Arb rerun. The exact extension `diag(M,-1)`
   proves that any one positive finite section remains insufficient for global
   Weil positivity. The next obligation is
   `CofinalPoleNeutralGuinandWeilIntervalLDLCertificatesHaveVanishingNegativeDefect`.
2. **Collatz:** `ExactlyThreeValuationOnesOtherwiseTwoCycleExclusion` closes
   every contracting word with exactly three valuation-one entries and all
   remaining entries two. A cyclic-gap bound proves `1<B/D<3` for `h>=13`;
   exact integer enumeration closes all 645 words at `h=8..12`. The next
   obligation is
   `NoContractingValuationWordWithExactlyFourOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `SignedSubhorizonSurvivorSignatureIndistinguishability`
   proves that a prime pair and a bad pair can have identical truncated
   roughness signatures through the exact shared gate. Therefore signed and
   nonlinear post-processing of the same bits cannot restore primality labels.
   The next obligation is
   `SignedVonMangoldtSubhorizonResidualIsBelowExplicitMajorMainForEveryLargeEvenTarget`.
4. **Twin Prime:** `QuantizedTwinProjectorIntervalRoundingCertificate` proves
   the exact compatible count range for any certified projector interval.
   A rigorous lower endpoint greater than zero already certifies at least one
   twin because `Delta in 4 Z_{>=0}`; `[0,4]` is sharply ambiguous. The next
   obligation is
   `CertifiedStrictlyPositiveTwinProjectorLowerEndpointOnInfinitelyManyPredeclaredDyadicBlocks`.

Machine audit: four exact theorems, one newly closed infinite cycle stratum,
one attributed primary-artifact audit, four rejected or corrected routes, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-187](positive-ray-threeone-signature-interval.md).
한국어 보고서: [TICKET-187](positive-ray-threeone-signature-interval.ko.md).

## 2026-08-02 TICKET-186 Quantifier and Margin Corrections

TICKET-186 continues from TICKET-185 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `FiniteCodimensionCoercivityIsNotNecessaryForNonnegativity`
   proves that the positive compact model `diag(1/n)` has quotient infimum
   zero after removing any finite-dimensional subspace. Uniform coercivity is
   therefore not a necessary generic consequence of Weil nonnegativity. The
   next obligation is
   `WeilQuadraticFormNonnegativityOnExplicitPoleNeutralCoreWithVanishingCertifiedDefect`.
2. **Collatz:** `ExactlyTwoValuationOnesOtherwiseTwoCycleExclusion` closes the
   full contracting stratum with exactly two valuation-one entries and all
   remaining entries two. For `h>=9`, oddness and `1<B/D<3` rule out affine
   divisibility; the 22 cases at `h=5..8` are exact finite exceptions. The next
   obligation is
   `NoContractingValuationWordWithExactlyThreeOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `BadSurvivorLayerCakeAndNonnegativeSubhorizonNoGo` proves
   `sum_(y<tau) B_N(y)=sum_bad gamma_N(a)` and shows every nonzero nonnegative
   subhorizon weighting remains composite-contaminated. The next obligation is
   `SignedPrimeWeightedBadSurvivorCorrelationHasUniformSubHorizonPowerSaving`.
4. **Twin Prime:** `QuantizedTwinProjectorAndFixedRelativeMarginNoGo` proves
   `A00-A10-A01+A11=4C`, so positivity has the exact four-unit threshold. An
   abstract one-twin ledger has relative margin `4/A00 -> 0`, rejecting a fixed
   normalized margin as necessary. The next obligation is
   `PredeclaredCubicRoughSignedTypeIIMainDominatesRemainderOnInfinitelyManyDyadicBlocks`.

Machine audit: four exact theorems, one newly closed infinite cycle stratum,
four rejected targets, zero conjecture resolutions, and zero computational
failures.

English report: [TICKET-186](codimension-twoone-layercake-quantization.md).
한국어 보고서: [TICKET-186](codimension-twoone-layercake-quantization.ko.md).

## 2026-08-02 TICKET-185 Exact Resolution Barriers

TICKET-185 continues from TICKET-184 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:** `TwoNeutralMomentAutocorrelationSpectralEscapeNoGo` constructs
   a normalized, compactly supported, positive-definite autocorrelation family
   satisfying both pole-neutral moments while its Fourier probability mass
   escapes every fixed compact band. The next obligation is
   `WeilQuadraticFormCoercivityModuloSpectralTranslationsOnExplicitPoleNeutralCore`.
2. **Collatz:** `SingleValuationOneOtherwiseTwoCycleExclusion` proves for every
   `h>=3` that the primitive period `(1,2,...,2)` has coprime affine numerator
   and cycle denominator, excluding the whole infinite stratum. It also
   withdraws universal first descent as a “smaller” auxiliary because
   TICKET-172 proved it Collatz-equivalent. The next obligation is
   `NoPrimitiveContractingValuationWordWithExactlyTwoOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility`.
3. **Goldbach:** `TargetSpecificGoldbachFactorHorizonEquivalence` identifies
   the exact least-factor cutoff `tau_N` at which every non-prime candidate
   pair for a fixed even `N` disappears. Reaching `tau_N` is a finite decision
   procedure, not an analytic proof. The next obligation is
   `SubHorizonPrimeWeightedBadSurvivorCancellationBelowTargetMargin`.
4. **Twin Prime:** `IntegerGranularityAndOneSidedBlockCertificate` proves that
   the one-sided remainder inequality is exactly positivity and that symmetric
   absolute domination is impossible when expected block mass is at most one
   half. The next obligation is
   `CubicRoughOneSidedJointLiouvilleBlockMarginOnUnboundedScales`.

The replay uses four spectral carriers, Collatz horizons through 128, six
Goldbach targets through 50,000, and seven Twin block widths on
`[100000,362144)`. These diagnostics check the formulas but do not close an
infinite conjecture. Machine audit: four exact theorems, four rejected targets,
three decisive route corrections, zero conjecture resolutions, and zero
computational failures.

English report: [TICKET-185](spectral-cycle-factor-granularity.md).
한국어 보고서: [TICKET-185](spectral-cycle-factor-granularity.ko.md).

## 2026-08-02 TICKET-184 Information-Sufficiency Audit

TICKET-184 continues from TICKET-183 and keeps every parent conjecture at
`open_not_proven`.

1. **Riemann:**
   `FiniteMomentCancellationDoesNotGiveUniformAbelDesmoothing` gives an
   explicit family that cancels any fixed finite number of polynomial Fourier
   moments while its Abel mean vanishes and its original norm remains one.
   The next obligation is
   `NormalizedWeilAdmissibleConeHasUniformFourierTailTightnessFromFullMellinConstraints`.
2. **Collatz:** `CounterexampleDichotomyAndMinimalCyclePrefixBarrier` separates
   nontrivial cycles from unbounded orbits and proves a necessary least-cycle
   prefix barrier. The barrier is not sufficient, and cycle exclusion alone
   is not a full proof. The next obligation is
   `EveryPositiveOddIntegerAboveOneHasAnAcceleratedIterateBelowItsStart`.
3. **Goldbach:** `SquarefreeWheelFactorizationAndCompositeImpostorNoGo` proves
   the exact CRT local factor and constructs a composite-only copy of every
   unit residue. The next obligation is
   `GrowingWheelPrimeWeightedMinorErrorIsUniformlyBelowTheLocalSingularMargin`.
4. **Twin Prime:** `PositiveRootMassSufficesAndCantelliExceptionalMassIsSharp`
   proves that recurring positive total block mass is enough and that
   every-leaf positivity is unnecessarily strong. The next obligation is
   `PrimePairBlockMainTermDominatesParityRemainderOnAnUnboundedDisjointSequence`.

Finite diagnostics include 12 exact moment-cancellation cases, first descent
for every odd start through one million, exact wheel factorization through
`Q=1155` with 480 composite impostors, and a finite block containing 2,298
twin pairs. Machine audit: four exact theorems, four rejected or corrected
routes, two decisive-target corrections, zero conjecture resolutions, and
zero computational failures.

English report: [TICKET-184](information-sufficiency-route-correction.md).
한국어 보고서: [TICKET-184](information-sufficiency-route-correction.ko.md).

## 2026-08-02 TICKET-183 Uniform-Transfer Audit

TICKET-183 continues from the four TICKET-182 open nodes and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `AbelFejerDesmoothingCertificateAndHighFrequencyNoGo` proves
   an exact three-term Abel-Fejer-H1 certificate and a high-frequency family
   showing that the desmoothing remainder cannot be omitted. The next
   obligation is `PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus`.
2. **Collatz:** `PrimitiveWordReductionAndMonotoneValuationExclusion` proves
   that repeated valuation words have exactly the same cycle-divisibility
   status as their primitive root and excludes every non-fixed cycle with
   `v_j>=2`. The remaining words are primitive, contracting, and contain
   `v=1`. The next obligation is
   `NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility`.
3. **Goldbach:** `ExactFourierErrorIdentityAndSparseDensityNoGo` proves an
   exact target-indexed finite-group Fourier error identity and then applies
   an absolute error budget for a sufficient positivity margin. Parseval shows
   that a sparse constant-density prime model cannot pass that phase-blind
   budget. The next obligation is
   `GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin`.
4. **Twin Prime:** `WeightedHaarVarianceIdentityAndNegativePathSquareCertificate`
   proves the exact weighted variance decomposition and a pathwise sufficient
   positivity condition. A one-zero-leaf family refutes global Haar-energy
   promotion. The next obligation is
   `PrimePairNegativeHaarPathSquareStaysBelowRootMargin`.

Finite diagnostics cover Abel prime proxies through 100,000; 488,280 Collatz
words with 87,380 words in the completely excluded monotone stratum; exact
strong-Goldbach enumeration through 50,000; and 2,298 actual twin pairs on
`[100000,362144)`. These ranges do not close an infinite quantifier. Machine
audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-183](abel-primitive-spectral-haar.md).
한국어 보고서: [TICKET-183](abel-primitive-spectral-haar.ko.md).

## 2026-08-02 TICKET-182 Representation-Aligned Localization Audit

TICKET-182 continues from the four TICKET-181 open nodes and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `FejerH1TailCertificateAndRawPrimeEnergyNoGo` replaces a
   global Lipschitz constant by an exact periodic `H1` multiplier budget. It
   also proves that a raw `Lambda(n)/sqrt(n)` cosine proxy has divergent
   derivative energy and that grid values plus derivatives do not determine
   the global budget. The next obligation is
   `SmoothedPoleNeutralWeilSymbolHasWeightedH1EnergyBelowCoreMargin`.
2. **Collatz:** `AcceleratedCycleIffAffineDivisibility` proves that a positive
   valuation word is an exact accelerated cycle iff `D=2^S-3^h>0` divides its
   ordered affine numerator `B(w)`. The next obligation is
   `OnlyConstantTwoValuationWordsSatisfyPositiveAffineCycleDivisibility`.
3. **Goldbach:** `WeightedTranslationModulusCertificateAndRmsSpikeNoGo`
   sharpens the adjacent-target budget to a Fejer-weighted uniform translation
   modulus and proves RMS translations can hide one exceptional target. The
   next obligation is
   `GoldbachResidualHasWeightedUniformTranslationModulusBelowLowPassMarginOnEveryLargeBlock`.
4. **Twin Prime:** `WeightedSiblingContrastIdentityAndMeanPathNoGo` identifies
   each additive block increment with an exact mass-weighted sibling contrast
   and proves level-averaged variation can hide one bad path. The next
   obligation is
   `PrimePairSiblingContrastHasUniformCarlesonPathBudgetBelowCancellationMargin`.

Finite diagnostics cover seven RH Fejer orders and raw prime proxies through
100,000; 488,280 Collatz words over `{1,...,5}` through horizon eight; actual
Goldbach prime-indicator translations through 20,000; and 2,298 actual twin
pairs on `[100000,362144)`. These ranges do not close any infinite quantifier.
Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-182](sobolev-divisibility-translation-sibling.md).
한국어 보고서: [TICKET-182](sobolev-divisibility-translation-sibling.ko.md).

## 2026-08-02 TICKET-181 Regularized-Localization Audit

TICKET-181 continues from the four TICKET-180 no-go nodes and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `LipschitzFejerTailCertificateAndSampledRegularityNoGo`
   proves that a global Lipschitz modulus converts a finite Fejer mean into a
   uniform tail certificate, while a uniform-grid slope estimate can miss
   `A sin(Q theta)` completely. The next obligation is
   `PoleNeutralWeilSymbolHasCertifiedModulusWhoseFejerBudgetFitsBelowCoreMargin`.
2. **Collatz:** `OddCylinderSlackQuantizationAndCycleEqualityObstruction`
   proves that natural-cylinder descent slack is a multiple of `2^(S+1)`.
   Thus a sub-quantum lower bound plus equality exclusion forces strict
   descent; the fixed point proves equality exclusion is indispensable. The
   next obligation is
   `EveryFirstContractingNonterminalCylinderHasPositiveSlackQuantum`.
3. **Goldbach:** `DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo`
   proves that a discrete Fejer low pass plus an adjacent-target modulus gives
   every-target positivity and rejects the TICKET-180 spike. The next
   obligation is
   `ParityAliasedGoldbachResidualHasCertifiedDiscreteModulusBelowFejerMarginOnEveryLargeBlock`.
4. **Twin Prime:** `DyadicPathVariationLocalizationAndScaleL2NoGo` proves a
   root anchor plus pathwise `l1` oscillation controls every dyadic block and
   constructs a sharp family where maximum-edge and pathwise `l2` variation
   vanish while one bad leaf remains. The next obligation is
   `PrimePairBlockZeroModeRatioHasSummableDyadicPathOscillationBelowCancellationMargin`.

Finite diagnostics cover six RH orders, 87,380 Collatz words over
`{1,2,3,4}` through depth eight plus the fixed point, five Goldbach model
cycles plus exact counterexample search through 100,000, and five Twin tree
depths. These ranges do not close any infinite quantifier. Machine audit: four
exact theorems, four rejected routes, four proof DAGs, zero conjecture
resolutions, and zero computational failures.

English report: [TICKET-181](regularized-localization-quantized-slack.md).
한국어 보고서: [TICKET-181](regularized-localization-quantized-slack.ko.md).

## 2026-08-02 TICKET-180 Finite-Information Localization Audit

TICKET-180 audits the four open nodes left by TICKET-179 and keeps every parent
conjecture at `open_not_proven`.

1. **Riemann:** `FiniteToeplitzMomentIndeterminacyAndTailEnvelopeNecessity`
   proves that an arbitrary hidden Fourier mode can preserve every observed
   Toeplitz section while violating the global symbol margin. The next
   obligation is
   `ArithmeticWeilTailHasCertifiedUniformHighFrequencyEnvelopeBeyondObservedBand`.
2. **Collatz:** `ValuationLayerPermutationNoGoAndOrderedAffinePrefixIdentity`
   proves the exact ordered affine numerator and exhibits natural cylinders
   with equal valuation layers but different first-descent times. The next
   obligation is
   `OrderedCylinderTransferHasUniformDescentOutsideExplicitFiniteExceptionalSet`.
3. **Goldbach:** `MeanSquareExceptionalSpikeNoGoForEveryTargetPositivity`
   proves that normalized RMS and exceptional density can both vanish while a
   single target remains negative. The next obligation is
   `ParityAliasedMinorHasUniformLInfinityDeficitBelowMajorMainOnEveryDyadicBlock`.
4. **Twin Prime:** `GlobalCenteredEnergyNoGoForUniformBlockCancellation`
   proves that global centered-energy saturation can approach one while a
   single block stays fully aligned. The next obligation is
   `PrimePairHaarCenteredEnergySaturatesDiagonalUniformlyOnEveryLargeDyadicBlock`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-180](finite-information-localization.md).
한국어 보고서: [TICKET-180](finite-information-localization.ko.md).

## Preserved 2026-08-02 TICKET-179 Representation-Adequacy Audit

TICKET-179 continues the four open nodes left by TICKET-178 and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `BoundedToeplitzSymbolCertificateAndAbsoluteSummabilityNoGo`
   proves that a bounded real Fourier symbol controls every finite Toeplitz
   section even when the absolute coefficient sum diverges. The next obligation
   is `PoleNeutralWeilWhitenedTailHasBoundedRealFourierSymbolBelowCoreMargin`.
2. **Collatz:** `AdaptiveValuationLayerCompletenessAndFixedDepthIncompleteness`
   proves exact layer-cake recovery of a completed first descent and constructs
   an infinite first-descent cylinder family missed by every fixed valuation
   depth. The next obligation is
   `EveryAperiodicNonDescendingOrbitAccumulatesAdaptiveValuationLayerSurplusBeyondExactCorrection`.
3. **Goldbach:** `DiscreteTargetPositivityCertificateAndContinuousInterpolationNoGo`
   proves exact cyclic target evaluation and constructs, for every tested even
   grid size, an interpolant positive on all targets but negative between them.
   The next obligation is
   `ParityAliasedMinorHasUniformDiscreteEvenTargetDeficitBelowMajorMain`.
4. **Twin Prime:** `CrossGramCenteringIdentityAndPairwiseIncoherenceNoGo`
   proves zero-mode saving equivalent to centered-energy saturation. An
   orthonormal family has zero pairwise coherence but no zero-mode saving. The
   next obligation is
   `PrimePairHaarCenteredEnergySaturatesDiagonalAtPowerSavingRate`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-179](symbol-adaptive-discrete-centering.md).
한국어 보고서: [TICKET-179](symbol-adaptive-discrete-centering.ko.md).

## 2026-08-02 TICKET-178 Summability, Low-Bit, Frequency-Split, and Zero-Mode Audit

TICKET-178 continues the four open nodes left by TICKET-177 and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `SummableToeplitzTailCertificateAndNonsummableProfileNoGo`
   proves the exact `s>1` summability threshold for a phase-blind absolute
   Toeplitz tail. The next obligation is
   `PoleNeutralWeilWhitenedTailHasSummableOffDiagonalProfileBelowCoreMargin`.
2. **Collatz:** `LowBitOccupancyDescentCriterionAndFixedHorizonMixingNoGo`
   turns modulo 4 and 8 occupancy into an exact descent sufficient condition.
   The starts `2^m-1` refute every fixed-horizon mixing replacement. The next
   obligation is
   `EveryAperiodicNonDescendingOrbitCrossesLowBitOccupancyThreshold`, followed
   by separate nontrivial-cycle exclusion.
3. **Goldbach:** `FrequencySplitSobolevCertificateAndGlobalBudgetNoGo` splits
   high-frequency sup control from low-frequency energy and derivative
   control. A strictly positive cosine counterfamily refutes necessity of the
   unsplit global diagnostic. The next obligation is
   `ParityAliasedMinorHasUniformDyadicSplitSobolevBudgetBelowMajorMain`.
4. **Twin Prime:** `CrossGramZeroModeCertificateAndAbsolutePhaseErasureNoGo`
   identifies the signed all-plus zero mode as a sufficient aggregate operator
   certificate. Roots-of-unity counterfamilies prove absolute Gram data are
   insufficient. The next obligation is
   `PrimePairHaarSignedCrossGramZeroModeHasPowerSavingRelativeToDiagonalEnergy`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-178](toeplitz-lowbit-frequency-split-zeromode.md).
한국어 보고서: [TICKET-178](toeplitz-lowbit-frequency-split-zeromode.ko.md).

## 2026-08-02 TICKET-168 Fixed-Core, Least-Realizer, Phase-Minimax, and Parity-Main Audit

TICKET-168 continues the four open nodes left by TICKET-167 and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `FixedMomentCorrectorCoreBridgeAndCutoffVaryingConstraintNoGo`
   proves that a fixed bounded finite-rank corrector preserves nesting and
   density of a constrained form core. Alternating cutoff constraints have
   positive restrictions but miss a fixed negative witness. The next obligation
   is `CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore`.
2. **Collatz:** `LeastRealizerDescentMonotonicityAndModularShadowNoGo` proves
   the descent gap increases by `2(2^S-3^m)` between consecutive natural
   realizers, reducing one word to its least realizer. The exact finite audit
   reaches length 20, counts 7,553,085 candidates, and finds zero bad realizers.
   The next obligation is
   `UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord`.
3. **Goldbach:** `PhaseBlindSpectralL1MinimaxAndMagnitudeOnlyNoGo` proves
   spectral `l1` is the sharp worst-case uniform bound from Fourier magnitudes.
   Every finite phase-blind diagnostic remains above one despite observed tails
   below one. The next obligation is
   `UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin`.
4. **Twin Prime:** `FinestParityHalfCorrelationIdentityAndCancellationTargetNoGo`
   proves the finest parity projection contains exactly half of the odd gap-two
   correlation. Cancelling it would cancel half the target. The next obligation
   is `PositiveLinearOddVonMangoldtFinestParityPairing`.

한국어 요약: TICKET-168은 리만의 고정 neutral-core 보정, 콜라츠 최소
실현값 단조성, 골드바흐 phase-blind spectral-`l1` 최소최대 한계,
쌍둥이 소수 parity 절반 주항을 정확히 증명했다. cutoff 가변 제약,
실현 가능성 제약을 버린 affine modular shadow만의 실제 word 하강 판정,
magnitude-only Goldbach 개선, 최미세 Twin
주항 상쇄 경로는 폐기했다. 실제 Weil LDL, 모든 Collatz word의 최소
실현값 하강, target-dependent Goldbach phase 상쇄, 양의 von Mangoldt
parity 주항은 여전히 미증명이다. 해결된 추측 수는 0이다.

[TICKET-168 bilingual report](fixedcore-leastrealizer-phase-paritymain.md)에
정확한 정리, 계산, no-go 반례, 문헌 경계와 proof DAG를 기록한다.

## 2026-08-01 TICKET-167 Cofinal, Residue-Count, Besov, and Parity-Scale Audit

TICKET-167 continues the four open nodes left by TICKET-166 and keeps every
parent conjecture at `open_not_proven`.

1. **Riemann:** `CofinalNestedCoreCertificateBridgeAndNonDenseSubspaceNoGo`
   proves that interval lower bounds are needed only on a cofinal subsequence
   of a nested dense form core. The exact countermodel
   `diag(-1,1,1,...)` rejects positivity on a nested but non-dense family. The
   next obligation is
   `CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore`.
2. **Collatz:** `ExactBadRealizerCountAndWordwiseDensityZeroNoGo` gives a
   closed formula for every fixed contracting word's non-descending natural
   realizers. Finiteness makes wordwise density zero automatic and therefore
   insufficient. The finite exact audit counts 1,120,444 candidate words
   through length 18 and finds zero bad realizers. The next obligation is
   `UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord`.
3. **Goldbach:** `BesovOneShellAnchorBridgeAndAlignedScaleL2NoGo` replaces an
   observed high-frequency error by a dyadic shell-Cauchy sufficient bound.
   Aligned disjoint frequency blocks refute scale-`l2` promotion. Every finite
   Farey diagnostic certificate remains above one, so the route is not closed.
   The next obligation is `UniformBinaryGoldbachBesovOneTailBelowAnchorMargin`.
4. **Twin Prime:** `FinestParityScaleExtractionAndCoarseControlNoGo` proves
   that the finest support-two product-Haar projection of the shift-two
   selector has exact energy `(N-2)/2`. Coarse-scale control alone can therefore
   miss a linear correlation. The next obligation is
   `PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving`.

한국어 요약: TICKET-167은 리만 인증을 조밀한 cofinal core로 줄이고,
콜라츠 고정 word의 bad realizer 수를 정확히 세며, 골드바흐의 필요한
Besov-`l1` shell 예산과 현재 유한 gate 실패를 분리하고, 쌍둥이 소수
선택자의 최미세 parity scale이 선형 에너지를 가짐을 증명했다. 실제
Weil LDL cofinal family, 모든 first-crossing word의 양의 residue slack,
1 아래의 산술 Goldbach shell budget, prime-weighted finest/coarse 상쇄는
여전히 미증명이다. 해결된 추측 수는 0이다.

[TICKET-167 bilingual report](cofinal-residue-besov-parity.md)에 정확한
정리, 계산, 실패한 gate, no-go 반례, 문헌 경계와 proof DAG를 기록한다.

## 2026-08-01 TICKET-166 Tail-Adaptive, Bandlimited, and Shifted-Diagonal Audit

TICKET-166 continues the four exact open nodes left by TICKET-165 and keeps
every parent conjecture at `open_not_proven`.

1. **Riemann:** `PositiveTailDiagonalCoreBridgeAndAmbiguousBandNoGo` composes a
   positive omitted tail with interval-certified Galerkin lower bounds. A
   cubic diagonal cutoff turns a tail order `(2N+1)log(T)/T` into
   `O(log N/N^2)`, while an exact scalar pair proves that the tail budget alone
   cannot decide a truncated eigenvalue in `[-B,0)`. The next obligation is
   `IntervalCertifiedTruncatedWeilLowerBoundAtVanishingTailScaleOnEveryNestedCore`.
2. **Collatz:** `StartAdaptiveFinalExcessReductionAndZeroExcessMagnitudeNoGo`
   proves that first-crossing non-descent implies `3n(2^t-1)<m`. The residual
   window is therefore `O(log(1+m/n))`, and only `t=0` remains when `m<=3n`.
   The next obligation is
   `UniformNaturalResidueSlackInsideStartAdaptiveExcessWindow`.
3. **Goldbach:** `BandlimitedAnchorClosureAndFullBandwidthSpikeNoGo` combines
   Bernstein sampling with a uniform low-pass error to obtain a pointwise
   gate. A unit spike has full DFT support and defeats every anchor set that
   omits it. The next obligation is
   `UniformDyadicLowPassApproximationAndAnchorMarginForBinaryMinorDeficit`.
4. **Twin Prime:** `ShiftedDiagonalHaarDualityAndCenteredPermutationNoGo`
   identifies the exact product-Haar dual of the noncyclic `n,n+2` selector.
   Its double-centered projection has zero margins but saturates the signed
   dual bound at linear scale. The next obligation is
   `PrimeWeightedShiftedDiagonalHaarPairingPowerSavingBeyondParity`.

한국어 요약: TICKET-166은 리만 양의 꼬리의 대각 core 연결, 콜라츠의
시작값 적응형 excess 창, 골드바흐의 대역 제한 표본화, 쌍둥이 소수의
shifted-diagonal Haar 쌍대성을 정확히 분리했다. 실제 모든 Weil core의
interval 하한, 콜라츠 자연수 residue slack, 모든 dyadic shell의
Goldbach 저주파 균일 근사, prime-weighted signed diagonal power saving은
여전히 미증명이다. 해결된 추측 수는 0이다.

[TICKET-166 bilingual report](tail-adaptive-bandlimited-diagonal.md)에 정확한
정리, 계산, no-go 반례, 문헌 경계와 proof DAG를 기록한다.

## 2026-08-01 TICKET-165 Vanishing-Defect, Log-Tail, Variation, and Signed-Dual Audit

TICKET-165 attacks the four open nodes left by TICKET-164. It replaces one
unnecessary uniform target, reduces one infinite tail at every length, and
identifies the pointwise or signed information missing from two averaged
routes.

1. **Riemann:** `VanishingDefectCoreLimitBridgeAndUniformGapNoGo` proves
   nonnegativity from form-core convergence and a negative defect
   `epsilon_N -> 0`. The path-Laplacian witness has Rayleigh quotient
   `12/[n(n+1)]`, so a cutoff-independent positive spectral gap is not
   necessary. The next target is
   `ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect`.
2. **Collatz:**
   `UniformLogarithmicFinalExcessReductionAndConstantExcessNoGo` proves that
   `9(2^t-1)>m` closes every first-crossing natural realizer `n>=3`, leaving
   only `O(log m)` final excesses at every length. A near-critical exact
   family rejects any fixed-excess shortcut based on the same coarse affine
   envelope. The next target is
   `UniformResidueSlackForLogarithmicFirstCrossingExcessWindow`.
3. **Goldbach:**
   `SparseAnchorVariationPointwiseBridgeAndFiniteMomentSpikeNoGo` proves that
   anchor maximum plus local path variation below one is a pointwise
   no-exception certificate. A unit spike defeats every fixed finite
   normalized `Lp` moment. The next target is
   `UniformDyadicMinorDeficitAnchorMarginAndVariationDecay`.
4. **Twin Prime:** `SignedProductHaarDualityAndUnsignedEnergyNoGo` proves the
   weighted product-Haar Cauchy dual gate. The pair `H,-H` has identical
   unsigned square energy but model counts `2,0`, so a signed prime-weighted
   error estimate below the main term is indispensable. The next target is
   `PrimeWeightedSignedProductCarlesonDualMarginBeyondParity`.

한국어 요약: RH의 양의 균일 gap을 필요조건에서 제거하고 소멸 음의
결함으로 교체했습니다. Collatz의 길이별 무한 final-valuation 꼬리는
로그 개수로 줄었지만 그 residue 창은 닫히지 않았습니다. Goldbach는
anchor와 변동을 함께 써야 점별 결론이 나오며, 고정 유한 moment만으로는
단일 예외를 배제할 수 없습니다. Twin은 무부호 에너지 대신 부호 있는
쌍대 오차가 main term보다 작다는 실제 gate가 필요합니다. 네 추측의
해결 수는 0입니다. 자세한 증명과 재현 명령은
[TICKET-165 vanishing-defect-logtail-variation-signed-dual](vanishing-defect-logtail-variation-signed-dual.md)에
있습니다.

## 2026-07-31 TICKET-164 Core-Eigen, First-Crossing, Pointwise, and Product Audit

TICKET-164 attacks the four open nodes left by TICKET-163 and tightens the
actual proof object on every track.

1. **Riemann:** `ConstraintCoreCompressionAndScalarCancellationNoGo`
   proves that finite positivity under admissibility constraints is exactly
   positivity of `U^T H U`. Positive trace, determinant, and one positive
   test value do not suffice. The next target is
   `UniformGuinandWeilConstraintCoreMinimumEigenvalueLowerBound`.
2. **Collatz:**
   `FirstContractingLayerFiniteCertificateAndFinalValuationBound` proves that
   each fixed first-crossing prefix has only finitely many final valuations
   that can fail descent for `n>=3`. Exact replay closes every word through
   length 17, totaling 464,921 candidate residues. Final-valuation margin
   monotonicity is refuted by `(1,3)` versus `(1,4)`. The next target is
   `UniformFirstContractingLayerResidueSlack`.
3. **Goldbach:**
   `PointwiseIntegralExceptionEquivalenceAndL2NonNecessityNoGo` proves
   `G_N>0` exactly when `E_N^-/M_N<1`. The previous shell `L2<1` condition
   remains sufficient but is not necessary; an all-positive family has
   unbounded `L2` budget. The next target is
   `UniformDyadicPointwiseMinorDeficitStrictlyBelowOne`.
4. **Twin Prime:** `ProductHaarParsevalAndEqualScaleTensorNoGo` proves exact
   independent-scale product-Haar Parseval and gives anisotropic matrices
   with positive full energy but zero equal-scale tensor energy. The next
   target is `UniformPrimeWeightedProductCarlesonPowerSavingBeyondParity`.

한국어 요약: 리만에서는 상쇄 합계를 최소 고유값 문제로 교정했고,
콜라츠에서는 각 길이의 무한 final-valuation tail을 affine 부등식으로
닫은 뒤 길이 17까지 완전 검사했습니다. 골드바흐에서는 너무 강한
shell `L2` 목표를 정확한 점별 문턱으로 바꾸었고, Twin에서는 행·열
scale을 독립화했습니다. 네 추측의 해결 수는 0입니다. 자세한 증명과
재현 명령은
[TICKET-164 core-eigen-first-crossing-pointwise-product](core-eigen-first-crossing-pointwise-product.md)에
있습니다.

## 2026-07-31 TICKET-163 Local-Certificate, Realizer, Trace, and Carleson Audit

TICKET-163 attacks the four open nodes left by TICKET-162 and corrects the
localization level of each target.

1. **Riemann:** `FinitePrimeTraceH1ContinuityAndAbsoluteMassNoGo` proves an
   explicit `H1` continuity bound at every fixed positive prime trace. The
   absolute coefficient mass diverges, so the resulting coefficient-mass
   majorant cannot supply uniformity. The next target is
   `CancellationAwareUniformGuinandWeilTraceBoundOnConstraintCore`.
2. **Collatz:**
   `AffineCorrectionMajorizationAndNaturalRealizerCouplingNoGo` proves that
   the front-loaded word maximizes affine correction at fixed length and
   total valuation. The exact length-17 word realized by `165` ends at `167`
   despite smaller correction, refuting fixed-length transfer. It is not a
   Collatz counterexample because the first step is `165 -> 31`. The next
   target is `FirstContractingLayerNaturalRealizerDescent`.
3. **Goldbach:** `DyadicIntegralExceptionCertificateAndDilutedSpikeNoGo`
   proves that a normalized negative-error budget below one on every dyadic
   shell excludes every exception. One unit spike per growing shell has mean
   tending to zero but preserves one exception. The next target is
   `UniformDyadicNormalizedNegativeMinorBudgetBelowOne`.
4. **Twin Prime:** `LocalDyadicVarianceIdentityAndGlobalDilutionNoGo` proves
   exact variance telescoping on every dyadic square. An embedded checkerboard
   has global energy density tending to zero while its local density remains
   one. The next target is
   `UniformPrimeWeightedLocalCarlesonPowerSavingBeyondParity`.

한국어 요약: TICKET-163은 전역 평균이나 uncoupled 극값을 점별·국소
결론으로 승격하는 네 경로를 교정했습니다. 리만에서는 유한 trace의
연속성과 발산하는 절댓값 상계를 분리했고, 콜라츠에서는 exact natural
residue가 correction 순서와 결합되어야 함을 길이 17 반례로
확정했습니다. 골드바흐는 shellwise `<1` 기준으로 목표를 약화하면서
평균 0 경로를 폐기했고, Twin은 전역 에너지 희석과 국소 Type-II
제어를 분리했습니다. 네 추측의 해결 수는 0입니다. 전체 증명과 재현
명령은
[TICKET-163 local-certificate-realizer-trace-carleson](local-certificate-realizer-trace-carleson.md)에
있습니다.

## 2026-07-27 TICKET-162 Form-Norm, Explicit Baker, Integral, and Multiscale Audit

TICKET-162 attacks the four open nodes left by TICKET-161.

1. **Riemann:** `ResolvedH2ToH1TransportAndUniformH1BallNoGo`
   proves effective `H2`-to-`H1` Fourier transport under `N/L -> infinity`
   and refutes a uniform rate on the whole `H1` unit ball. The remaining
   target is actual uniform `H1` continuity of the finite Guinand-Weil forms.
2. **Collatz:** `ExplicitMinimalFrontLoadedFamilyClosureAndCoverageNoGo`
   combines Matveev's explicit constant with certified continued fractions
   to close the selected minimal front-loaded family for every `m>=2`.
   Its share among equal-length positive valuation compositions tends to
   zero, so the remaining target is a natural-orbit coverage theorem.
3. **Goldbach:** `IntegralExceptionalSetMomentBridgeAndUnitSpikeSharpness`
   proves that a target-normalized negative-error moment below one excludes
   every zero representation count, and that one is the sharp gate. The
   tested prime DFT budgets remain above one.
4. **Twin Prime:**
   `DyadicIncidenceEnergyDecompositionAndFixedBinNoGo` gives the exact
   martingale energy identity and proves that one fixed incidence partition
   can miss all fine checkerboard dependence. A uniform multiscale bound
   with prime-producing weights remains open.

한국어 요약: TICKET-162는 리만 가설의 `H2→H1` 수송, 콜라츠 선택
계열의 모든 길이 폐쇄, 골드바흐 적분 예외예산의 정확한 `<1` gate,
쌍둥이 소수 Type-II incidence의 dyadic 에너지 분해를 증명했습니다.
동시에 전체 `H1` 단위공 수송, 선택 Collatz 계열의 전체 궤도 포괄,
예산 1 이상의 평균 Goldbach 추정, 고정 Twin binning을 각각
폐기했습니다. 네 추측 자체의 해결 수는 여전히 0입니다. 전체 증명과
재현 명령은
[TICKET-162 formnorm-explicitbaker-integral-multiscale](formnorm-explicitbaker-integral-multiscale.md)에
있습니다.

## 2026-07-26 TICKET-144 Exact Certificate and Target-Strength Audit

TICKET-144 attacks the four TICKET-143 targets at their quantifier and
necessity boundaries before allocating another large finite search.

1. **RH:** `NestedGramSchurPivotCertificateAndFinitePrefixExtensionNoGo`
   proves that every nested Gram section is positive exactly when every exact
   Schur pivot is positive. Any bounded positive prefix admits the unchanged
   extension `diag(G_N,-1)`, so finite-prefix promotion is retired. Attack
   `ExplicitWeilFormCoreSchurPivotLowerBound`.
2. **Collatz:** `GlobalWellFoundedRankIffCollatzTermination` proves that an
   unrestricted decreasing well-founded rank exists exactly when all
   accelerated odd orbits terminate. Hitting-time ranks are therefore
   circular. Attack `ExplicitLiftClosedFiniteDescriptionCollatzRank`, whose
   finite semantics, lift closure, and descent must be independent of
   termination.
3. **Goldbach:**
   `BoundedSignalLinearAbsoluteMartingaleVariationNoGo` constructs bounded
   dyadic vectors with absolute path variation `d/2`; the generic `K=56`
   budget is exceeded at depth 113 while the signed endpoint stays bounded.
   The construction is not a Goldbach residual. Attack
   `ArithmeticBinaryGoldbachSignedMartingaleCancellationK56`.
4. **Twin Prime:**
   `WalshL1SimplexBalanceIdentityAndAdversePartReduction` proves that full
   Walsh `L1` means two-sided balance of every parity class and that only
   `B=A10_+ + A01_+ + (-A11)_+` is needed for
   `N-- >= (A00-B)/4`. Attack
   `UniformCubicRoughAdverseWalshPartContraction`.

All four conjectures remain open. The exact code, tests, JSON, proof DAGs, and
bilingual report preserve `conjecture_resolution_count=0`.

한국어 요약: TICKET-144는 RH의 유한 prefix 승격을 Schur pivot 전역
하한으로 교정하고, Collatz의 제약 없는 rank가 추측과 동치임을 증명하며,
Goldbach의 일반 절대변동 목표를 bounded 반례족으로 폐기하고, Twin의
전체 Walsh 양방향 균형을 adverse 성분만 제어하는 조건으로 약화한다.
네 난제는 모두 `open_not_proven`이며 해결 수는 0이다.

## 2026-07-25 TICKET-143 Form-Core, Period-Floor, Martingale, and Walsh Correction

TICKET-143 audits the four TICKET-142 highest-risk nodes before allocating
another large finite search.

1. **RH:** `ClosedFormCoreFiniteSectionBridgeAndHilbertDenseNoGo` proves the
   exact form-core promotion theorem. The graph family
   `G_N=diag(2n^2)-11^T` is positive for every `N` and Hilbert dense, but the
   full closed form has the negative witness `(1,0)`. Hilbert density is
   therefore retired; attack
   `ExplicitWeilFormCoreCompressionCertificateFamily`.
2. **Collatz:** the cited published `K>7.2e10` odd-period floor makes period
   15,601 obsolete. Its `a_0=1`, `S=24,727` raw composition count is
   `binom(24725,15599)`, a 7,069-digit integer, and equal `(k,S)` does not
   determine the affine numerator. Attack
   `PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness`.
3. **Goldbach:** the exact dyadic martingale identity reconstructs every
   residual point from the root mean and scale-normalized path differences.
   A constant signal has bounded points, zero wavelets, and root coefficient
   `sqrt(n)`, so the raw uniform Haar cap is retired. Attack
   `UniformBinaryGoldbachRootMeanPlusDyadicPathVariationBelow56`.
4. **Twin Prime:** Walsh-Hadamard inversion proves
   `A00-A10-A01+A11=4*pi_2[X,2X]`; the previous one-sided gap is exactly the
   desired block positivity and is circular as a separate bridge. Attack
   `UniformCubicRoughWalshL1ContractionBelowOne`.

All four conjectures remain open. The exact code, tests, JSON, proof DAGs, and
bilingual report preserve `conjecture_resolution_count=0`.

한국어 요약: TICKET-143은 더 큰 계산보다 먼저 네 목표의 위상과 논리
강도를 교정한다. RH에는 form-core가 필요하고, Collatz 15,601주기는 공개
하한 아래이며, Goldbach raw Haar 계수는 척도 정규화가 잘못됐고, Twin
단측 gap은 원래 블록 쌍둥이 존재와 정확히 동치다. 다음 목표는 각각
실제 Weil form-core 압축, 공개 주기 하한을 반영한 자연수 코드
well-foundedness, Goldbach root 평균과 dyadic 경로변동, cubic-rough
Walsh `L1` 수축이다.

## 2026-07-25 TICKET-142 Typed Targets and Direction Correction

TICKET-142 audits the four TICKET-141 open nodes before spending more
computation on them.

1. **Riemann:** shifted moments factor exactly into the spectral edge and
   `q`-effective rank. A scalar family proves that `O(log rank)` without its
   coefficient is not an automatic positivity certificate. The actual
   projected Weil finite sections and tail convergence must be defined first.
2. **Collatz:** the product window gives an upper bound on a hypothetical
   primitive-cycle minimum, not the lower bound proposed by the previous next
   target. The forced successor and distinct terms sharpen that upper bound,
   but period 15,601 still leaves 4,340,106 possible minima above `2^28`.
3. **Goldbach:** robust recovery is invariant under an honest simultaneous
   basis/error-set transform. Haar localization gives an exact route from
   coefficient budget 23 to pointwise residual below 56, but the corresponding
   arithmetic coefficient theorem is open.
4. **Twin Prime:** cubic roughness reduces primality exactly to Liouville
   parity and yields `4*pi_2=A00-A10-A01+A11`. Unsigned minor-arc cancellation
   cannot determine the missing one-sided parity combination.

한국어 요약: TICKET-142는 더 큰 유한 계산보다 먼저 네 다음 목표의
논리적 형식을 교정한다. RH에는 명시적 유한절단과 tail 수렴 계약이
필요하고, Collatz product window의 하한 방향은 폐기되며, Goldbach
직교화는 실제 공동 오차집합을 바꾸지 않는 한 난이도를 줄이지 못한다.
Twin Prime에서는 양의 gap-2 질량을 Liouville parity 혼합항으로
분해한다. 네 난제는 모두 `open_not_proven`이다. 전체 증명과 재현
명령은 `docs/effective-rank-cycle-direction-haar-liouville.md`에 있다.

## 2026-07-30 TICKET-141 Directional and Robustness Correction

TICKET-141 attacks the four TICKET-140 open nodes and separates one exact
advance from each still-missing arithmetic theorem.

1. **Riemann:** shifted trace moments provide a one-sided positivity
   certificate. Opposite scalar spikes have identical unshifted even moments,
   so the unshifted sequence cannot completely decide positivity.
2. **Collatz:** avoiding automatic relaxed-window vacuity requires a
   period-dependent minimum floor with asymptotic slope at least
   `1/(3 log 2)`. This is necessary, not a cycle exclusion.
3. **Goldbach:** the endpoint raw-moment dual on normalized power-of-two nodes
   has norm greater than `2^(q(q-1)/2)`. A localized orthogonal arithmetic dual
   is required; no Goldbach residual is bounded here.
4. **Twin Prime:** the analytic large sieve gives arbitrary-coefficient
   bilinear cancellation at the fixed `sqrt(2)` phase. Uniform minor arcs,
   the actual Vaughan or Mobius decomposition, the parity obstruction, and
   positive exact-gap-two mass remain open.

한국어 요약: TICKET-141은 네 경로에 방향성과 강건성 조건을 추가한다.
RH의 짝수 moment 부호 손실, Collatz의 느린 moving floor, Goldbach raw
moment의 폭발적 dual norm, Twin Prime의 단일 위상 한계를 각각 정확히
분리했다. 네 난제는 모두 `open_not_proven`이다. 전체 증명과 재현 명령은
`docs/one-sided-moving-floor-robust-dual-and-large-sieve.md`에 있다.

## 2026-07-17 TICKET-130 Computability and Route-Optimality Correction

TICKET-130 keeps the strongest TICKET-129 reductions and applies the
proof-or-counterexample rule to their proposed next steps.

1. **Riemann:** every rational-bump core Weil value is a computable real. With
   the earlier continuity and density theorems, a strict-negative witness is
   semidecidable. Universal nonnegativity is not proved.
2. **Collatz:** finite valuation-cap language extinction is refuted as a proof
   target. The mechanical word `a_j=C_(j+1)-C_j` survives every depth and every
   finite prefix has infinitely many positive realizers. The language still has
   an unconditional exponential mass bound
   `(65/48)rho^j`, `rho=0.9466204159695351...`; density zero is not emptiness.
3. **Goldbach:** exact Euler-product arithmetic proves `K=56` is the largest
   integer available to the current fixed-cutoff, uniform-coefficient endpoint
   architecture. The actual pointwise `K=56` residual estimate remains open.
4. **Twin Prime:** the additive block defect factors exactly as
   `D(Y)=Q_YR(Y)`. The dimensionless coefficient target is
   `limsup R(2^j)<2/23`, still followed by the parity and exact-gap barriers.

한국어 요약: TICKET-130은 유한 계산을 더 늘리지 않았다. RH 반례 탐색의
계산 가능성을 닫고, Collatz의 잘못된 유한 소멸 목표를 정확한 생존 word로
폐기하며, Goldbach 상수 개선 경로의 한계를 증명하고, Twin 증분 결함을
`2/23` 상대 임계값으로 환원했다. 어느 난제도 해결하거나 반증하지 않았다.
전체 증명과 재현 명령은
`docs/computability-cap-language-optimality.md`에 있다.

## 2026-07-17 TICKET-129 Exact Core and Necessary-Condition Reduction

TICKET-129 advances the four tracks without treating a larger finite range as
an infinite proof.

1. **Riemann:** finite Gaussian-rational combinations of a standard smooth
   bump form a countable dense core in `C_c^infinity(R)`, and their
   autocorrelations are dense inside the autocorrelation image. This respects
   the TICKET-126 separation no-go: no density in the whole ambient space is
   claimed. TICKET-128 makes the prime side finite for every core element.
   Certified archimedean values and nonnegativity remain open.
2. **Collatz:** a hypothetical least counterexample is at least `2^28` and the
   exact orbit-product identity forces `S_j<=ceil(j log2 3)` for every
   `j<=2^29`. At 256 steps the prefix-cap language has exact cylinder mass
   approximately `4.7634970603e-9`, but compatible words survive. This is a
   necessary condition, not a contradiction.
3. **Goldbach:** exact atanh-series intervals prove
   `214/5<log(4*10^18)<43`, while elementary integer comparisons prove
   `B<21/10`. Together with `A>1.31917`, a pointwise residual theorem with
   `K=56` is sufficient, with exact margin
   `23019645297/2140000000000`. The residual theorem remains open.
4. **Twin Prime:** the exact identity
   `Q_X-Q_Y=(Delta A-Q_Y Delta K)/K_X` identifies the minimal within-block
   defect. A monotone cumulative countermodel with denominator doubling still
   reaches `Q=1.84` between two `0.92` endpoints. Since TICKET-128 gives only
   an endpoint limsup, the exact target is
   `limsup_j D(2^j)<0.08`, plus parity and gap-two positivity.

한국어 요약: TICKET-129는 RH의 열거 가능한 자기상관 핵심집합, Collatz 최소
반례의 첫 `2^29`단계 valuation cap, Goldbach `K=56` 충분조건의 완전 유리수
인증, Twin Prime 구간 내부 증분 결함 항등식을 증명했다. 각각의 결정적 다음
정리는 여전히 미증명이며 네 난제 중 해결되거나 반증된 것은 없다. 자세한
증명과 재현 명령은 `docs/enumerable-core-valuation-cap-endpoint-budget.md`에
있다.

## 2026-07-17 TICKET-128 Premise Reduction

TICKET-128 applies the proof-or-counterexample rule to four different failure
modes instead of extending one plot.

1. RH compact support removes the infinite prime tail exactly: only `p^m<=B`
   remains. A finite prime sum is not yet a certified Weil value because core
   density and the archimedean interval remain open.
2. The 4,027,109 Collatz objects from TICKET-127 are unresolved lift cylinders,
   not integer counterexamples. Direct replay closes every nontrivial
   representative below `2^28`, with no step-cap survivor. The missing object
   is still an unbounded-prefix theorem or uniform well-founded rank.
3. A rational tail product proves `2*C2>1.31917`. This changes the Goldbach
   residual target from the earlier `K<42.83274372223497` budget to the weaker
   sufficient statement `K<=55`; it does not prove that residual estimate.
4. A concrete Twin sequence satisfies every frozen dyadic endpoint recurrence
   while exceeding one at infinitely many midpoints. Endpoint-only
   interpolation is therefore false. The exact repair needs a within-block
   envelope with `0.92*c+delta<1` before parity and exact-gap arguments can be
   considered.

The canonical report is
`docs/finite-core-prefix-constant-interpolation.md`. All four conjecture
resolution counters remain zero.

## 2026-07-15 Registered Twin Persistence Attempt

TICKET-119 applies the exact proof-or-counterexample discipline to the strongest current Twin route. The 16M rule was committed as `87bdcf9` before execution. Failure would have refuted the frozen claim that TICKET-118's canonical adjacent-pair finite closure persists at the first doubling. The first execution instead passed with finite lower expression `+1,479,021.8` and normalized margin `19.7322%`.

This result rejects neither the Twin Prime Conjecture nor the missing eventual theorem. It also does not prove either one. The proof obligation is now explicit:

```text
Find fixed delta>0 and X0 such that, for every X>=X0,
canonical signed endpoint budget + boundary + variation
    <= (1-delta) * independently positive comparison term.
```

The first subproblem is `UniformLowDivisorCanonicalPairDispersion`, because the outer-divisor group 257-1023 contributes 59.14% of the 16M canonical budget. The counterexample oracle must search for an unbounded Vaughan-realizable scale sequence that violates every fixed margin; a later isolated finite failure is only a route counterexample at that scale.

## 2026-07-15 Low-Divisor Lemma Falsification

TICKET-120 does not add another horizon. It attacks the first TICKET-119 sublemma by proving the exact two-block triangle identity and immediately testing an unjustified strengthening.

```text
true:  paired low-pair budget <= singleton low-pair budget
false: paired low-pair budget <= (1-eta) singleton budget
       for some universal eta>0 under only PSD Gram hypotheses
```

The exact counterexample uses equal positive means and identical unit vectors. Its Gram matrix is rank-one positive semidefinite and its saving is zero. This is a counterexample to the candidate lemma, not to Twin Prime.

The 16M audit also rejects the working explanation that mean-sign opposition drives the observed saving: scalar mean cancellation supplies only `0.0069%` of the saving. The corrected target is `VaughanLowDivisorDenominatorSummedAngleGap`, which must derive a denominator-summed centered-angle gap from actual signed Möbius/divisor arithmetic.

## 2026-07-15 Balance-Angle Target Correction

TICKET-121 falsifies the idea that an angle gap by itself yields a uniform low-pair saving. If `z0=u` and `z1=-epsilon*u`, then the cosine is always `-1` but the centered saving fraction is `2epsilon/(1+epsilon)`, which tends to zero. Conversely, equal norms do not help when the angle tends to zero. Both factors are necessary.

The exact rationalization is

```text
w(||z0||+||z1||-||z0+z1||)
  = 2w(||z0||||z1||-Re<z0,z1>)
    /(||z0||+||z1||+||z0+z1||).
```

The corrected theorem target is:

```text
VaughanLowDivisorWeightedBalanceAngleDefectGap
```

It must place a fixed positive fraction of denominator weight on pairs having both comparable norms and a fixed cosine gap. The exploratory rational certificate `balance>=1/8`, `angle gap>=1/2`, mass at least `1/2` implies centered saving at least `1/32`. These thresholds were not preregistered. Existing rows satisfy the mass test, but this does not prove its eventual persistence. Moreover `1/32` fails to close the frozen 8M full budget while it closes the frozen 16M budget with other terms held fixed. The full theorem must therefore control all canonical groups and boundary terms, not only the first pair.

## Result Summary

### Riemann Hypothesis

Direct RH counterexample search was not attempted in this lab because certified zeta-zero isolation requires a dedicated analytic/numeric verifier.

What was attempted instead:

```text
candidate theorem counterexample
finite-prefix obstruction
contrapositive zero-exclusion route
```

The lab constructs a symmetric surrogate zero model containing an off-critical quartet. The first 80 Li-type coefficients in this surrogate stay nonnegative in the current run. This does not disprove RH. It shows that a finite Li/Jensen/Hermite prefix is not a proof route unless it is upgraded to a uniform all-index theorem.

Next theorem:

```text
RH-TICKET-17 UniformOffCriticalDetector
```

Required breakthrough:

```text
Assume an off-critical zero exists. Construct a Li-type coefficient, kernel, or explicit-formula test functional that becomes negative, uniformly over all heights and all off-critical displacements.
```

한국어 설명: 리만가설은 유한 개의 zero나 유한 개의 Li 계수 확인으로 끝나지 않는다. 반례 방향으로 가려면 "critical line 밖 zero가 있으면 반드시 감지되는 전역 검출기"가 필요하다.

### Collatz Conjecture

Direct search:

```text
starts checked: 100,000
direct counterexample found: no
max steps seen: n = 77,031, steps = 350
```

Candidate proof route falsified:

```text
Every odd accelerated Collatz step descends immediately.
```

This is false. For example, `3 -> 5`, `7 -> 11`, `11 -> 17` under the accelerated odd map. Therefore a one-step descent proof cannot work.

Next theorem:

```text
CO-TICKET-17 ResidueDebtAutomatonLift
```

Required breakthrough:

```text
Build a residue-debt automaton whose rank may temporarily increase but must decrease over every closed or escaping block, then prove that the finite automaton lifts to all integers.
```

한국어 설명: Collatz는 네 문제 중 가장 CEGIS에 잘 맞는다. 직접 반례가 없더라도, 약한 descent 주장은 곧바로 깨진다. 따라서 "한 번에 감소"가 아니라 "debt를 기록하고 블록 단위로 감소"하는 rank가 필요하다.

### Goldbach Conjecture

Direct search:

```text
even n <= 100,000 checked
direct counterexample found: no
```

Candidate proof route stressed:

```text
A uniform lower bound can ignore residue-profile worst cases.
```

This is too weak. The lab identifies hardest even numbers by representation count and normalized margin. These are not Goldbach counterexamples; they are counterexamples to careless lower-bound arguments.

Next theorem:

```text
GB-TICKET-17 ResidueProfileExplicitCutoff
```

Required breakthrough:

```text
For each residue profile, prove an explicit representation-count lower bound whose cutoff lies below the finite verification range.
```

한국어 설명: 골드바흐는 반례 탐색 자체보다 "가장 위험한 짝수 profile"을 찾는 것이 중요하다. 그래야 해석적 lower bound의 상수 손실을 어디서 줄여야 하는지 보인다.

### Twin Prime Conjecture

Finite direct refutation is not possible in the same way, because the negation is eventual:

```text
there exists N such that no twin primes occur after N
```

The lab found:

```text
twin pairs up to 200,000: 2,160
```

Candidate proof route falsified:

```text
bounded gaps imply exact gap 2
```

The gap distribution contains many wider bounded gaps. In the current run, bounded-gap mass up to gap 40 is dominated by wider gaps, so any proof that converts bounded gaps to twin primes without an exact gap-2 projection is invalid.

Next theorem:

```text
TP-TICKET-17 ExactGapTwoProjection
```

Required breakthrough:

```text
Construct a parity-barrier-resistant lower bound for exact gap 2, not merely for some bounded gap.
```

한국어 설명: 쌍둥이 소수에서 가장 위험한 착각은 bounded gap을 gap 2로 바꾸는 것이다. 이 변환은 자동으로 되지 않는다. exact gap-2 mass를 따로 분리하는 정리가 필요하다.

## Unified Method

For every future candidate theorem, PrimeProject should store:

```json
{
  "direct_counterexample": {},
  "candidate_counterexamples_found": {},
  "contrapositive_route": "...",
  "missing_infinite_bridge": "...",
  "next_theorem_to_attempt": "...",
  "claim_boundary": "not a proof"
}
```

Promotion rule:

```text
A candidate can move toward proof status only if:
1. direct counterexample search finds no counterexample in the committed range;
2. candidate-theorem counterexample search does not falsify the route;
3. the contrapositive or infinite bridge is stated exactly;
4. no finite-only, heuristic independence, or target-equivalent axiom is used;
5. the bridge is formalized or accepted as an external theorem.
```

## Current Priority

The strongest next move is:

```text
CO-TICKET-17 ResidueDebtAutomatonLift
```

Reason:

```text
Collatz failures produce concrete residue states, transitions, and SCCs. This gives AI a real counterexample-guided loop rather than only vague analytic pressure.
```

The second priority is:

```text
GB-TICKET-17 ResidueProfileExplicitCutoff
```

Reason:

```text
Goldbach has a clear finite-plus-infinite proof architecture: finite verification below N0 and explicit lower bound above N0.
```

The third priority is:

```text
TP-TICKET-17 ExactGapTwoProjection
```

The fourth priority is:

```text
RH-TICKET-17 UniformOffCriticalDetector
```

## Ticket 17 Breakthrough Attempt Results

Generated artifact:

```text
data/open-problem/ticket17-breakthrough-attempts.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-17-uniform-offcritical-detector.json
data/open-problem/collatz/co-ticket-17-residue-debt-automaton-lift.json
data/open-problem/goldbach/gb-ticket-17-residue-profile-explicit-cutoff.json
data/open-problem/twin-prime/tp-ticket-17-exact-gap-two-projection.json
```

Current verdict:

```text
breakthrough_attempts_open_no_resolution
```

한국어 요약: TICKET-17은 네 난제를 풀었다고 주장하지 않는다. 대신 각 문제의 다음 무한다리 정리를 더 날카롭게 만들었다.

1. RH: finite Li-type detector가 off-critical surrogate를 충분히 빨리 잡는지 실험했다. 현재 결과는 finite detector만으로는 부족하며, 전역 effective detector theorem이 필요하다는 쪽이다.
2. Collatz: accelerated odd trajectory의 residue-debt를 추적했다. 표본상 하강 압력은 보이지만, residue-debt state 전체를 덮는 lifting theorem이 없다.
3. Goldbach: residue profile별 representation lower envelope를 추적했다. finite margin은 양수지만, profile별 analytic error term을 이겨야 한다.
4. Twin Prime: exact gap 2 mass와 wider bounded-gap mass를 분리했다. bounded gap 신호는 wider gap에 크게 오염되므로 exact gap projection theorem이 필요하다.

## Ticket 18 Reduction Lab Results

Generated artifact:

```text
data/open-problem/ticket18-reduction-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-18-finite-prefix-camouflage.json
data/open-problem/collatz/co-ticket-18-valuation-branch-cover.json
data/open-problem/goldbach/gb-ticket-18-explicit-error-budget.json
data/open-problem/twin-prime/tp-ticket-18-bounded-gap-countermodel.json
```

Current verdict:

```text
reduction_attempts_open_no_resolution
```

한국어 요약: TICKET-18은 네 난제를 풀었다고 주장하지 않는다. 대신 "증명처럼 보이는 단축로"를 실제 반례 모델이나 정확한 환원 계산으로 공격한다.

1. RH: high-height off-critical surrogate quartet가 finite Li-prefix에서 거의 보이지 않는 camouflage 현상을 만든다. 따라서 유한 prefix 양성만으로는 리만가설을 증명할 수 없고, height-uniform detector 또는 tail theorem이 필요하다.
2. Collatz: 샘플 궤적 대신 exact accelerated valuation word를 열거했다. 각 branch는 `T^k(n)=(3^k n+c)/2^a` 꼴의 정확한 affine map을 갖는다. 많은 branch는 수축하지만, expanding branch를 전역적으로 낮은 rank로 보내는 branch graph theorem이 아직 필요하다.
3. Goldbach: finite count를 Hardy-Littlewood scale과 residue profile별 margin으로 바꾸어 explicit analytic error budget을 산출했다. 반례는 없지만, 이 margin을 이기는 공개 상수 기반 lower-bound theorem이 없으면 증명이 아니다.
4. Twin Prime: 각 관측 twin pair의 두 번째 소수를 삭제하는 bounded-gap countermodel을 만들었다. 이 모델은 exact gap 2를 0으로 만들면서도 bounded gap 대부분을 유지한다. 따라서 bounded-gap 정리만으로 twin prime conjecture를 증명하는 경로는 차단된다.

Next decisive target:

```text
CO-TICKET-19 BranchGraphRankSearch
```

Reason:

```text
Collatz now has the most concrete finite-to-infinite bridge candidate: exact valuation branches plus a possible well-founded rank over the branch graph.
```

## Ticket 19 Proof Pressure Lab Results

Generated artifact:

```text
data/open-problem/ticket19-proof-pressure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-19-tail-uniformity-pressure.json
data/open-problem/collatz/co-ticket-19-branch-graph-rank-search.json
data/open-problem/goldbach/gb-ticket-19-local-obstruction-elimination.json
data/open-problem/twin-prime/tp-ticket-19-admissibility-vs-exact-gap.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-19는 직접 증명, 반례 탐색, 대우법 후보를 더 압박한다. 결론은 네 문제 모두 여전히 open이다.

1. RH: off-critical surrogate quartet를 height `10,000,000`까지 올리면 첫 200개 Li-type prefix에서 최대 효과가 약 `8.0004e-10`까지 작아진다. 이는 finite prefix positivity가 RH 증명이 될 수 없고 height-uniform tail theorem이 필요하다는 점을 강화한다.
2. Collatz: odd accelerated step 길이 32까지 exact valuation-word density를 계산했다. 32-step에서도 expanding word density가 약 `0.032454323536` 남고, all-ones valuation word는 모든 고정 길이에 대해 확장한다. 따라서 fixed-block contraction 증명은 실패하며 branch graph rank가 필요하다.
3. Goldbach: mod `6, 30, 210, 2310`에서 unit prime residue sum이 모든 target residue를 덮는다. 즉 테스트한 범위에서는 local modular obstruction이 없고, 남은 문제는 explicit analytic lower bound다.
4. Twin Prime: twin pattern은 prime modulus `2..47`에서 locally admissible이지만, 삭제형 countermodel은 exact gap 2를 `2994 -> 0`으로 만들면서 bounded gap의 약 `88.461835%`를 유지한다. 따라서 local admissibility와 bounded-gap 생존은 twin prime infinitude가 아니다.

Next decisive target:

```text
CO-TICKET-20 ValuationPrefixRankCEGIS
```

Reason:

```text
The strongest current path is no longer fixed-length Collatz descent. It is a counterexample-guided search for a well-founded rank over exact valuation prefixes.
```

## Ticket 20 Valuation-Prefix Lab Results

Generated artifact:

```text
data/open-problem/ticket20-valuation-prefix-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-20-uniform-tail-contract.json
data/open-problem/collatz/co-ticket-20-valuation-prefix-rank-cegis.json
data/open-problem/goldbach/gb-ticket-20-local-multiplicity-barrier.json
data/open-problem/twin-prime/tp-ticket-20-admissibility-constant-vs-deletion.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-20은 "유한 계산을 더 늘리는 방식"이 아니라, 네 난제에서 약한 증명 경로가 왜 실패하는지 더 정확한 certificate로 남긴다.

1. RH: finite Li-prefix camouflage를 uniform tail contract 문제로 바꿨다. high-height off-critical surrogate가 유한 prefix에서 약하게 보이는 현상은 유지되며, 실제 증명에는 zero height와 Li index를 동시에 제어하는 tail theorem이 필요하다.
2. Collatz: all-ones accelerated valuation prefix를 길이 64까지 정확한 residue certificate로 만들었다. 길이 64의 대표 residue는 `0x1ffffffffffffffff`, 즉 `-1 mod 2^65`이고, `T^64(n)=(3^64 n + (3^64-2^64))/2^64` branch는 asymptotic multiplier가 약 `1.86140372879e11`이다. 이것은 Collatz 반례가 아니라, fixed-length contraction 증명 경로의 강한 반례다.
3. Goldbach: mod `6, 30, 210, 2310`에서 모든 target residue가 unit prime-residue pair로 덮이며, mod `2310`에서도 최소 ordered unit-pair count가 `135`다. 따라서 이 범위에서는 local congruence obstruction이 아니라 analytic lower bound가 본질이다.
4. Twin Prime: prime modulus `2..47`의 partial singular product는 양수이고 `2C2` 근사도 양수지만, deletion model은 exact gap 2를 `2994 -> 0`으로 만든다. local constant는 필요 조건이지 무조건적 infinitude proof가 아니다.

Next decisive target:

```text
CO-TICKET-21 TwoAdicBranchExclusion
```

Reason:

```text
The all-ones branch is visibly the positive-integer shadow of the 2-adic fixed point -1. A serious Collatz route must prove how such expanding 2-adic shadows are excluded or ranked down for all positive integers.
```

## Ticket 21 Two-Adic Branch Lab Results

Generated artifact:

```text
data/open-problem/ticket21-two-adic-branch-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-21-prefix-evasion-quantifier.json
data/open-problem/collatz/co-ticket-21-two-adic-branch-exclusion.json
data/open-problem/goldbach/gb-ticket-21-witness-spectrum.json
data/open-problem/twin-prime/tp-ticket-21-deletion-persistence-ladder.json
```

Current verdict:

```text
proof_pressure_open_no_resolution
```

한국어 요약: TICKET-21은 Collatz의 가장 단순한 2-adic obstruction인 all-ones branch를 좁은 의미에서 배제한다. 이것은 전체 Collatz 증명이 아니라, 하나의 무한 2-adic branch가 양의 정수 반례가 될 수 없다는 부분 결과다.

1. RH: finite Li-prefix countermodel pressure를 height별로 다시 계량했다. 결론은 동일하다. 유한 prefix 확인은 uniform tail theorem 없이는 RH 증명이 될 수 없다.
2. Collatz: 양의 홀수 `n`에 대해 `s=v2(n+1)`이면 all-ones accelerated branch를 최대 `s-1`단계만 따라갈 수 있다. 길이 128 shadow `2^129-1`도 all-ones prefix 뒤 다음 valuation에서 탈출한다. 무한 all-ones branch는 2-adic `-1`이고 양의 정수가 아니다.
3. Goldbach: 200,000 이하 직접 반례는 없고, hardest smallest-witness case는 `194470 = 383 + 194087`이다. 이 finite witness spectrum은 분석적 lower bound를 대체하지 않는다.
4. Twin Prime: deletion countermodel을 1,000,000까지 ladder로 반복했다. exact gap 2는 `8169 -> 0`이 되지만 bounded gaps는 약 `89.55%` 유지된다. bounded-gap shortcut은 계속 차단된다.

Next decisive target:

```text
CO-TICKET-22 MixedTwoAdicCylinderRank
```

Reason:

```text
The all-ones 2-adic branch is now isolated. The next useful Collatz step is to handle mixed expanding valuation cylinders and search for a rank that forces every such cylinder to escape into descent.
```

## Ticket 22 Negation Pressure Lab Results

Generated artifact:

```text
data/open-problem/ticket22-negation-pressure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-22-li-detector-horizon.json
data/open-problem/collatz/co-ticket-22-mixed-two-adic-cylinder-rank.json
data/open-problem/goldbach/gb-ticket-22-residue-deletion-obstruction.json
data/open-problem/twin-prime/tp-ticket-22-exact-gap-projection.json
```

Current verdict:

```text
negation_pressure_open_no_resolution
```

한국어 요약: TICKET-22는 네 난제를 "반례를 찾거나, 반례가 없다면 어떤 대우법/무한 정리가 필요한가"라는 관점으로 다시 공격한다. 결론은 아직 증명이나 반증이 아니다. 하지만 각 문제에서 약한 증명 전략이 어디서 깨지는지 더 분명해졌다.

1. RH: off-critical surrogate zero quartet은 결국 Li-type 계수에서 음의 신호를 만들지만, 강한 음의 신호가 나타나는 index가 테스트 범위에서 height squared 규모로 밀린다. 높이 500에서는 threshold `-1.0` 이하 신호가 index `694,274`에서 처음 보였다. 따라서 finite prefix proof는 uniform detector/tail theorem 없이는 계속 차단된다.
2. Collatz: 길이 12, valuation alphabet `{1,2,3}`에서 expanding valuation cylinder `42,502`개를 열거했고, 모두 exact 2-adic lift로 검증됐다. 비자명 positive cycle 후보는 나오지 않았고, known `1` cycle만 보였다. 이 결과는 Collatz 증명이 아니라, fixed-block descent 방식이 왜 실패하는지 보여준다.
3. Goldbach: modulus `30`, `210`, `2310`에서 unit residue sum이 모든 even residue를 덮는지 보았고, local obstruction은 없었다. `2310`에서는 가장 약한 even residue도 obstruction을 만들려면 unit residue class를 최소 `68`개 삭제해야 했다. 즉 단순 congruence obstruction으로 Goldbach 반례를 설명하기 어렵다.
4. Twin Prime: exact-gap projection을 deletion model에 적용했다. `2,000,000`까지 원래 exact gap 2는 `14,871`개였고 deletion model은 `0`개였지만, bounded gaps는 약 `89.96%` 유지됐다. 따라서 bounded-gap evidence와 exact twin-prime infinitude는 계속 분리해야 한다.

Next decisive target:

```text
CO-TICKET-23 CylinderRankCEGIS
```

Reason:

```text
Mixed expanding 2-adic cylinders are now exact finite objects, not vague heuristic examples. The next Collatz attack should synthesize a rank over cylinder transitions and search for a counterexample SCC where that rank cannot descend.
```

## Ticket 23 CEGIS Rank Lab Results

Generated artifact:

```text
data/open-problem/ticket23-cegis-rank-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-23-detector-bound-cegis.json
data/open-problem/collatz/co-ticket-23-cylinder-rank-cegis.json
data/open-problem/goldbach/gb-ticket-23-exceptional-set-cegis.json
data/open-problem/twin-prime/tp-ticket-23-parity-projection-cegis.json
```

Current verdict:

```text
cegis_rank_open_no_resolution
```

한국어 요약: TICKET-23은 증명 후보를 세운 뒤, 그 후보가 깨지는 반례성 구조를 먼저 찾는 CEGIS 방식으로 네 난제를 압박한다. 결론은 여전히 증명이나 반증이 아니다. 다만 “어떤 종류의 정리가 새로 필요하고, 어떤 쉬운 지름길은 실패하는가”가 더 구체화됐다.

1. RH: off-critical surrogate zero quartet에 대해 beta `{0.6, 0.75, 0.9}`, height `{20, 50, 100, 200}`을 테스트했다. 고정 Li-type prefix `180,000` 안에서 beta `0.6`, height `200`은 threshold `-1.0` 이하의 강한 음수 신호를 보이지 않았다. 이것은 RH 반례가 아니라, finite-prefix detector 증명 후보를 깨는 CEGIS witness다.
2. Collatz: odd residue quotient graph를 modulus `2^8, 2^10, 2^12, 2^14`에서 만들었다. 단순 integer-rank는 약 1/3의 edge에서 감소하지 않았고, `2^10`, `2^12` quotient에는 실제 positive cycle로 lift되지 않는 false cycle SCC가 나타났다. 따라서 필요한 정리는 lift-aware well-founded rank다.
3. Goldbach: `1,000,000` 이하 짝수에서 직접 반례는 없었다. hardest smallest-witness case는 `503222 = 523 + 502699`였다. 이 결과는 bounded exceptional set이 비어 있다는 계산 증거이며, 전체 증명에는 큰 N에서 representation count가 양수라는 explicit lower bound가 필요하다.
4. Twin Prime: deletion model은 `3,000,000`까지 exact gap 2를 `20,932 -> 0`으로 제거하지만, gap `<= 60` bounded mass의 약 `90.28%`를 유지한다. 따라서 bounded-gap 생존은 twin-prime infinitude를 증명하지 못하고, exact gap-2 하한 functional이 필요하다.

Next decisive target:

```text
CO-TICKET-24 LiftAwareRankOrExactGapWeight
```

Reason:

```text
TICKET-23 isolates two concrete next proof objects: a lift-aware Collatz rank that defeats false quotient cycles, and an exact-gap sieve weight that cannot be fooled by bounded-gap deletion models. These are narrower than trying to prove all four conjectures at once.
```

## Ticket 24 Bridge-Weight Lab Results

Generated artifact:

```text
data/open-problem/ticket24-bridge-weight-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-24-uniform-detector-budget.json
data/open-problem/collatz/co-ticket-24-lift-aware-rank-probe.json
data/open-problem/goldbach/gb-ticket-24-explicit-window-budget.json
data/open-problem/twin-prime/tp-ticket-24-exact-gap-weight-search.json
```

Current verdict:

```text
bridge_weight_open_no_resolution
```

한국어 요약: TICKET-24는 TICKET-23에서 분리된 두 핵심 후보, 즉 Collatz의 lift-aware rank와 Twin Prime의 exact-gap weight를 더 좁은 보조정리 형태로 압박한다. 결론은 여전히 네 난제의 증명이나 반증이 아니다. 하지만 “반례처럼 보이는 구조를 제거하는 부분 정리”와 “실제 증명에 필요한 exact statistic”이 더 선명해졌다.

1. RH: beta `{0.6, 0.75, 0.9}`, height `{100, 200, 500}`, search cap `1,000,000`에서 uniform detector budget을 만들었다. beta `0.6`, height `500`은 cap 안에서 threshold `-1.0` 이하 신호를 보이지 않았다. 따라서 fixed finite prefix proof는 다시 차단되고, height-uniform detector theorem이 필요하다.
2. Collatz: quotient graph를 `2^8, 2^10, 2^12, 2^14, 2^16, 2^18`까지 확장했다. `2^10`, `2^12`에서 나온 비자명 quotient cycle은 모두 affine lift audit에서 `globally_eliminated_expanding_word`로 제거됐고, `2^14` 이후 테스트한 quotient에는 known `1` cycle만 남았다. 이것은 전체 Collatz 증명이 아니라, false quotient cycle 제거 보조정리 후보다.
3. Goldbach: `2,000,000` 이하 직접 반례는 없었다. hardest first-witness case는 `1077422 = 601 + 1076821`였다. stride `2,000` sampled representation-count budget은 약한 finite window를 찾지만, 전체 증명에는 모든 충분히 큰 짝수에 대한 explicit lower bound가 필요하다.
4. Twin Prime: exact gap weight는 deletion model을 분리한다. `3,000,000`에서 exact gap 2 margin은 `20,932`이고 deletion model은 `0`이다. 반면 gap 2를 제외한 bounded-gap-only mass는 deletion model에서 약 `99.98%` 유지된다. 따라서 bounded-gap-only 통계는 거의 완전히 속고, exact gap 2 하한 정리가 필요하다.

Next decisive target:

```text
CO-TICKET-25 FormalAffineLiftLemma
```

Reason:

```text
TICKET-24 produces the most theorem-like local object so far: a quotient Collatz cycle can be globally eliminated when its exact valuation word has no positive integral affine fixed point. This can be formalized independently before attempting the full Collatz rank theorem.
```

## Ticket 25 Formal Lemma Kernel Results

Generated artifact:

```text
data/open-problem/ticket25-formal-lemma-kernel.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-25-finite-prefix-kernel.json
data/open-problem/collatz/co-ticket-25-affine-lift-lemma.json
data/open-problem/goldbach/gb-ticket-25-finite-exception-kernel.json
data/open-problem/twin-prime/tp-ticket-25-bounded-gap-counterkernel.json
```

Current verdict:

```text
formal_kernel_open_no_resolution
```

한국어 요약: TICKET-25는 TICKET-24의 계산을 “형식화 가능한 작은 kernel lemma”와 “깨진 shortcut”으로 추출한다. 결론은 여전히 네 난제의 증명이나 반증이 아니다. 하지만 Collatz 쪽에서는 실제로 독립 형식화가 가능한 부분 보조정리 후보가 나왔다.

1. RH: finite Li-prefix만 확인하는 proof route는 surrogate family에서 refuted된다. beta `0.6`, height `500`, prefix `1,000,000` 안에서 threshold witness가 없다. 이것은 RH 반례가 아니라 fixed-prefix proof 전략에 대한 kernel counterexample다.
2. Collatz: `2^10`, `2^12` quotient의 비자명 cycle 3개는 valuation word의 affine fixed point 조건을 통과하지 못한다. 모두 `globally_eliminated_expanding_word`이고, positive cycle 후보는 known `1`뿐이다. 이 kernel은 “해당 quotient false cycle은 양의 정수 cycle이 아니다”라는 부분 정리로 형식화할 수 있다.
3. Goldbach: `2,000,000` 이하 finite exception kernel은 counterexample count `0`이다. 이 kernel은 finite range만 닫고, 전체 추측에는 큰 짝수 전체에 대한 explicit lower bound가 따로 필요하다.
4. Twin Prime: bounded-gap-only 통계는 deletion counterkernel에 의해 refuted된다. exact gap 2를 모두 제거해도 gap 2 제외 bounded mass는 거의 보존된다. 따라서 twin-prime proof는 exact-gap-2 lower-bound functional을 사용해야 한다.

Next decisive target:

```text
CO-TICKET-26 LeanAffineLiftMicroProof
```

Reason:

```text
The Collatz affine lift kernel is now small enough to formalize as a standalone micro-proof: derive the affine fixed-point condition for a valuation word and prove that the listed expanding quotient cycles cannot be positive integer cycles.
```

## Ticket 26 Micro-Lemma Closure Results

Generated artifact:

```text
data/open-problem/ticket26-micro-lemma-closure.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-26-finite-universal-gap.json
data/open-problem/collatz/co-ticket-26-affine-fixed-point-proof.json
data/open-problem/goldbach/gb-ticket-26-finite-window-gap.json
data/open-problem/twin-prime/tp-ticket-26-bounded-gap-model-separation.json
```

Current verdict:

```text
micro_lemma_closed_full_conjectures_open
```

한국어 요약: TICKET-26은 네 난제를 풀었다고 주장하지 않는다. 대신 증명 시도 중 실제로 닫을 수 있는 작은 명제를 닫는다. 가장 의미 있는 진전은 Collatz다. quotient graph에서 cycle처럼 보였던 후보가 양의 정수 cycle이 되려면 exact valuation word의 affine fixed point 조건을 통과해야 한다는 산술 lemma를 독립 재계산했다.

1. RH: finite prefix만으로 universal RH-equivalent statement를 증명할 수 없다는 shortcut refutation을 닫았다. 남은 핵심은 unchecked tail을 덮는 all-height theorem이다.
2. Collatz: valuation word `w`의 accelerated composition은 `F_w(n)=(3^k n+c)/2^s`이다. 만약 `F_w(n)=n`인 양의 정수 cycle이면 `(2^s-3^k)n=c`가 필요하다. Ticket 24의 false quotient cycle 3개는 모두 `2^s-3^k <= 0`라서 positive integer fixed point가 불가능하다. positive control인 word `[2]`는 candidate `1`로 정확히 검증된다.
3. Goldbach: finite window certificate는 해당 범위만 닫는다. `2,000,000` 이하 반례 없음은 중요하지만, `2,000,002` 이후를 덮는 explicit large-even theorem 없이는 전체 증명이 아니다.
4. Twin Prime: exact gap 2를 모두 지워도 bounded-gap statistic이 유지되는 finite model separation을 닫았다. 따라서 bounded-gap-only 증명은 twin-prime infinitude를 증명하지 못한다.

Closed micro-lemma:

```text
CO-TICKET-26 AffineFixedPointNecessaryCondition
```

Remaining decisive target:

```text
CO-TICKET-27 LiftAwareNonCyclicRankSearch
```

Reason:

```text
The false-cycle part is now a closed arithmetic micro-lemma. The next real Collatz barrier is not cyclic fixed points; it is proving that every non-cyclic exact branch eventually descends under a well-founded lift-aware rank.
```

## Ticket 27 Rank-Frontier Lab Results

Generated artifact:

```text
data/open-problem/ticket27-rank-frontier-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-27-tail-uniformity-frontier.json
data/open-problem/collatz/co-ticket-27-lift-aware-noncyclic-rank.json
data/open-problem/goldbach/gb-ticket-27-tail-cutoff-frontier.json
data/open-problem/twin-prime/tp-ticket-27-exact-gap-rank-frontier.json
```

Current verdict:

```text
rank_frontier_open_no_resolution
```

한국어 요약: TICKET-27은 TICKET-26에서 닫힌 작은 보조정리를 다음 proof frontier로 밀어붙인다. 가장 중요한 결과는 Collatz다. `mod 2^b` quotient graph에서 known `1` cycle까지의 거리 rank는 대표 residue edge에서는 감소하지만, 실제 integer lift에서는 대량으로 깨진다. 따라서 "finite quotient rank만으로 Collatz를 증명한다"는 전략은 반례로 기각된다.

1. RH: finite prefix shortcut은 닫혔지만, 여전히 unchecked tail 전체를 덮는 uniform explicit-formula theorem이 없다. 다음 실험은 Li/kernel tail majorant의 symbolic separability counterexample 탐색이다.
2. Collatz: `2^12, 2^14, 2^16, 2^18` quotient rank를 테스트했다. `2^14` 이상에서는 quotient가 known `1` cycle로 모두 도달하지만, sampled integer lift에서 rank violation이 각각 `91,591`, `362,379`, `1,447,879`개 발생했다. residue `1`을 제외해도 violation이 남는다. 예를 들어 `mod 2^14`에서 residue `3`, lift `1`, integer `16387`은 quotient rank가 `2`에서 다음 residue rank `56`으로 증가한다.
3. Goldbach: finite window는 base case일 뿐이다. 전체 증명에는 finite certificate ceiling 아래로 내려오는 explicit large-even lower-bound theorem이 필요하다.
4. Twin Prime: bounded-gap deletion model을 통과하는 statistic은 여전히 부적격이다. 다음 proof frontier는 exact gap 2 삭제 시 반드시 붕괴하는 lower-bound functional이다.

Closed shortcut:

```text
finite quotient distance rank implies global Collatz descent
```

Remaining decisive target:

```text
CO-TICKET-28 LiftCoordinateDebtRankCEGIS
```

Reason:

```text
The quotient-only Collatz rank is now refuted by explicit lift counterexamples. A viable rank must include the lift coordinate, valuation debt, or exact 2-adic cylinder data and must decrease after a bounded debt window.
```

## Ticket 28 Trichotomy Descent Lab Results

Generated artifact:

```text
data/open-problem/ticket28-trichotomy-descent-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-28-mertens-tail-trichotomy.json
data/open-problem/collatz/co-ticket-28-lift-coordinate-debt-rank-cegis.json
data/open-problem/goldbach/gb-ticket-28-witness-cutoff-trichotomy.json
data/open-problem/twin-prime/tp-ticket-28-exact-gap-tail-trichotomy.json
```

Current verdict:

```text
trichotomy_descent_open_no_resolution
```

한국어 요약: TICKET-28은 사용자가 제시한 세 가지 증명 경로, 즉 반례 찾기, 반례가 없음을 증명하기, 대우법으로 증명하기를 각 난제에 명시적으로 적용한다. 이번 단계의 실질적 계산 진전은 Collatz exact cylinder descent다. 이는 단순 residue rank가 아니라 valuation word가 실제로 보장되는 `2^m` cylinder 전체에 대해 affine map을 계산하고, 그 cylinder의 모든 양의 lift가 시작값보다 작아지는지를 판정한다.

1. RH: `M(n)/sqrt(n)` Mertens stress를 `5,000,000`까지 계산했다. `n>=10,000`에서 최대 관측값은 `0.4629770364`이고 위치는 `24,185`이다. 이것은 RH와 양립하는 finite stress일 뿐이며, RH 반례나 증명은 아니다. 전체 증명에는 off-critical zero를 배제하는 tail-uniform theorem 또는 동등한 positivity theorem이 필요하다.
2. Collatz: `2^12, 2^14, 2^16, 2^18, 2^20, 2^22` exact cylinder를 검사했다. `2^22`에서는 `2,097,152`개 odd cylinder 중 `1,997,692`개가 all-lift descent로 닫혔고, `99,459`개는 `needs_split`으로 남았다. 또한 `1,000,000` 이하 odd start에서 자기보다 작아지지 않는 finite stopping counterexample은 발견되지 않았고, 최장 stopping-to-below-start는 `626,331`에서 `111` accelerated steps였다.
3. Goldbach: `2,000,000` 이하 모든 짝수에 대해 첫 소수 witness를 찾았다. 반례는 없었고, 가장 늦게 첫 witness가 나온 행은 `1,077,422 = 601 + 1,076,821`이다. 하지만 finite witness scan은 큰 짝수 전체에 대한 explicit lower-bound theorem을 대체하지 못한다.
4. Twin Prime: `10,000,000` 이하 exact gap-2 소수쌍은 `58,980`개이며 마지막 관측 pair는 `(9,999,971, 9,999,973)`이다. 이는 exact-gap finite evidence이지만, 무한히 많은 twin prime을 증명하려면 exact-gap-2 lower-bound functional이 필요하다.

Closed partial theorem:

```text
For every Collatz cylinder marked all_lift_descent in TICKET-28, the exact accelerated affine map sends every positive odd lift in that cylinder below its starting value.
```

Remaining decisive target:

```text
CO-TICKET-29 AdaptiveCylinderSplitTermination
```

Reason:

```text
The exact cylinder method now proves many full lift families, but the proof cannot be promoted while needs_split cylinders remain. The next theorem must show that adaptive splitting of only those cylinders terminates or yields a well-founded valuation-debt descent.
```

## Ticket 29 Adaptive Frontier Lab Results

Generated artifact:

```text
data/open-problem/ticket29-adaptive-frontier-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-29-tail-bridge-frontier.json
data/open-problem/collatz/co-ticket-29-adaptive-cylinder-split.json
data/open-problem/goldbach/gb-ticket-29-least-counterexample-cutoff.json
data/open-problem/twin-prime/tp-ticket-29-exact-gap-tail-pressure.json
```

Current verdict:

```text
adaptive_frontier_open_no_resolution
```

한국어 요약: TICKET-29는 TICKET-28의 `needs_split`을 직접 추적한다. Collatz에서는 전체 `2^28` odd cylinder를 전부 열거하지 않고, `2^12`에서 시작해 닫히지 않은 cylinder만 adaptive하게 쪼갰다. 이 접근은 계산량을 크게 줄이지만, 열린 frontier가 사라지지는 않았다. 따라서 “needs_split만 계속 쪼개면 자연스럽게 증명이 끝난다”는 순진한 전략은 현재 데이터로 지지되지 않는다.

1. RH: Mertens stress를 `10,000,000`까지 확장했다. `M(10,000,000)=1,037`이고, `n>=1,000,000`에서 최대 `|M(n)|/sqrt(n)`는 `0.4182454758` at `1,066,854`이다. 이것은 RH-compatible finite stress이며, 여전히 off-critical zero를 배제하지 못한다.
2. Collatz: adaptive split은 `base_bits=12`, `max_bits=28`에서 `8,687,144`개 상태를 처리했다. 이는 `2^28`의 full odd cylinder `134,217,728`개 중 약 `6.47%`만 본 것이다. 하지만 max depth에서 열린 frontier가 `3,618,400`개 남았고, full max space 기준 open fraction은 `0.02695918`이다. 이는 반례가 아니라, split termination theorem이 아직 없다는 정량적 장애물이다.
3. Goldbach: finite witness scan을 `5,000,000`까지 확장했다. 반례는 없었고 `2,499,999`개 짝수를 확인했다. 가장 늦게 첫 witness가 나온 행은 `3,807,404 = 751 + 3,806,653`이다. 전체 증명은 여전히 large-even tail lower bound에 달려 있다.
4. Twin Prime: exact gap-2 scan을 `20,000,000`까지 확장했다. twin pair count는 `107,407`, 마지막 관측 pair는 `(19,999,547, 19,999,549)`, 관측된 twin-start 간 최대 gap은 `2,190`이다. finite exact-gap persistence는 무한성을 증명하지 못한다.

Closed partial theorem:

```text
Every all_lift_descent state in the Ticket 29 adaptive Collatz run is an exact cylinder whose every positive odd lift descends below its starting value.
```

Refuted shortcut:

```text
Naive adaptive splitting alone is enough evidence for Collatz proof completion.
```

Remaining decisive target:

```text
CO-TICKET-30 ValuationDebtPotentialSynthesis
```

Reason:

```text
The adaptive frontier is smaller than full enumeration but does not vanish. The next proof attempt must synthesize a well-founded potential on open needs_split cylinders, or find a genuine obstruction/counterexample pattern inside that frontier.
```

### Ticket 30: Potential synthesis and obstruction search

Generated artifact:

```text
data/open-problem/ticket30-potential-synthesis-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-30-tail-majorant-synthesis.json
data/open-problem/collatz/co-ticket-30-valuation-debt-potential.json
data/open-problem/goldbach/gb-ticket-30-explicit-constant-ledger.json
data/open-problem/twin-prime/tp-ticket-30-exact-gap-functional.json
```

Aggregate verdict:

```text
potential_synthesis_open_no_resolution
```

한국어 요약: TICKET-30은 네 난제를 증명했다고 주장하지 않는다. 이번 단계의 목표는 TICKET-29에서 남은 열린 경계를 대상으로 “증명으로 이어질 수 있어 보이는 자연스러운 후보”를 실제로 합성하거나, 반대로 그 후보군이 실패한다는 반례 구조를 찾는 것이다. Collatz에서는 `needs_split` 상태들 사이에 항상 감소하는 valuation-debt potential을 만들 수 있는지 검사했다. 결과적으로 단순한 scalar linear potential 계열은 bounded adaptive frontier에서 모두 탈락했다.

1. RH: 더 큰 유한 Mertens scan 대신 tail majorant synthesis 문제로 목표를 바꿨다. 필요한 정리는 “off-critical zero가 있으면 유한 positivity violation으로 내려온다”는 tail-uniform bridge이다. 이 bridge는 아직 열려 있고, 유한 stress만으로 RH를 결정할 수 없다는 경계를 유지한다.
2. Collatz: exact-cylinder frontier에서 네 개 특징량 `coefficient_log2_debt`, `prefix_length`, `consumed_bits`, `next_valuation`에 대한 scalar linear potential을 시험했다. `full_candidate_max_bits=20`에서 candidate parent edge는 `32,951`개이고, `grid_search_max_bits=18`에서 grid parent edge는 `9,610`개이다. 정수 가중치 `[-2,2]^4` 전체에서 살아남은 weight는 `0`개였다. 가장 좋은 weight `[2,-1,-2,-1]`도 `6,826`개 violation, violation rate `0.39157871`을 남겼다. 이것은 Collatz 반례가 아니라, 단순 선형 potential 증명 전략의 bounded falsification이다.
3. Goldbach: finite witness scan의 확장이 아니라 explicit constant ledger로 전환했다. 필요한 남은 정리는 large-even tail에서 minor arc, major arc, exceptional character, singular series 하한을 하나의 검산 가능한 부등식 장부로 닫는 것이다.
4. Twin Prime: 더 긴 exact gap scan 대신 exact-gap functional synthesis로 전환했다. 필요한 남은 정리는 gap-2 선택자가 sieve/RMT/Fredholm 유사량에서 무한히 양의 질량을 유지한다는 tail theorem이다.

Closed partial theorem:

```text
No tested scalar linear valuation-debt potential over the four Ticket 30 Collatz features strictly decreases on every tested open adaptive-frontier edge.
```

Refuted shortcut:

```text
A simple one-dimensional linear potential in debt, prefix length, consumed bits, and next valuation is enough to close the Collatz adaptive frontier.
```

Remaining decisive target:

```text
CO-TICKET-31 LexicographicPiecewisePotentialCEGIS
```

Reason:

```text
The failed scalar potentials do not refute Collatz. They show that a viable proof, if it follows the current exact-cylinder path, probably needs a lexicographic, piecewise, nonlinear, or certificate-carrying descent invariant.
```

### Ticket 31: Feature-stutter obstruction

Generated artifact:

```text
data/open-problem/ticket31-feature-stutter-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-31-finite-stress-stutter.json
data/open-problem/collatz/co-ticket-31-feature-stutter-obstruction.json
data/open-problem/goldbach/gb-ticket-31-cutoff-ledger-stutter.json
data/open-problem/twin-prime/tp-ticket-31-parity-selector-stutter.json
```

Aggregate verdict:

```text
feature_stutter_open_no_resolution
```

한국어 요약: TICKET-31은 TICKET-30보다 더 강한 부정 결과를 준다. TICKET-30은 단순 선형 potential이 실패했다는 계산 결과였다. TICKET-31은 그 실패가 단순히 “선형이라서” 생긴 문제가 아님을 보인다. Collatz exact-cylinder frontier에는 부모와 자식이 같은 관측 특징량을 갖는 feature-stutter edge가 존재한다. 그러면 그 특징량만 입력으로 받는 어떤 함수도 부모와 자식을 구분할 수 없으므로, scalar, lexicographic, nonlinear, learned potential 모두 strict local descent를 만족할 수 없다.

1. RH: finite stress가 아무리 RH-compatible하게 반복되어도 zero-side tail theorem이 없으면 증명으로 승격되지 않는다. TICKET-31에서는 이것을 finite-stress stutter obstruction으로 명시했다.
2. Collatz: `base_bits=12`, `max_bits=21` adaptive frontier에서 parent edge `61,740`개, open child edge `112,860`개를 검사했다. 기본 네 특징량 `coefficient_log2_debt`, `prefix_length`, `consumed_bits`, `next_valuation`만 보면 indistinguishable edge가 `30,997`개, 비율 `0.27465001`이다. prefix word와 low residue까지 추가해도 같은 `30,997`개가 남는다. 따라서 이 local signature만 보는 strict descent proof는 불가능하다.
3. Goldbach: finite witness persistence는 explicit large-even cutoff ledger를 대체하지 못한다. 필요한 대상은 major arc, minor arc, singular series, exceptional character error를 하나의 양의 하한 부등식으로 닫는 검산 가능한 장부이다.
4. Twin Prime: bounded-gap 또는 averaged-pair 통계는 parity-blind stutter를 통과할 수 있다. exact gap 2를 강제하려면 wider gap-only countermodel을 배제하는 selector theorem이 필요하다.

Closed partial theorem:

```text
If an open Collatz exact-cylinder parent and an open child have identical local signature, then no deterministic scalar, lexicographic, nonlinear, or learned potential depending only on that signature can strictly decrease on that edge.
```

Proof sketch:

```text
Let S be the chosen local signature and let P be any deterministic potential that depends only on S.
For a feature-stutter edge, S(parent) = S(child). Therefore P(parent) = P(child).
Strict descent requires P(parent) > P(child), contradiction.
For a lexicographic tuple, the same equality holds componentwise.
```

Refuted shortcut:

```text
Replacing the failed Ticket 30 scalar linear potential with a black-box nonlinear or lexicographic function of the same local features is enough to close the Collatz frontier.
```

Remaining decisive target:

```text
CO-TICKET-32 StatefulMeasureOrAutomatonDescent
```

Reason:

```text
Scale-dependent features such as modulus bits or cylinder mass separate the tested stutters, but they are not by themselves well-founded pointwise descent proofs: bits may grow without a prior bound, and mass may tend to zero. The next proof candidate must supply either a compactness/measure theorem, a stateful automaton invariant, or an eventual-closure theorem for infinite stutter paths.
```

### Ticket 32: Stateful measure and stutter-budget certificate

Generated artifact:

```text
data/open-problem/ticket32-stateful-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-32-stateful-tail-certificate.json
data/open-problem/collatz/co-ticket-32-stateful-measure-descent.json
data/open-problem/goldbach/gb-ticket-32-stateful-cutoff-ledger.json
data/open-problem/twin-prime/tp-ticket-32-stateful-parity-selector.json
```

Aggregate verdict:

```text
stateful_measure_open_no_resolution
```

한국어 요약: TICKET-32는 TICKET-31이 막아낸 local feature-only descent를 우회하기 위해 stateful certificate를 시도한다. Collatz에서는 feature-stutter edge마다 “같은 signature가 앞으로 몇 단계 더 지속되는가”를 lookahead로 계산해 stutter budget으로 붙였다. 이 budget은 반복 low-child stutter 구간에서는 1씩 감소한다. 그러나 이것은 bounded frontier 안의 certificate이지, 모든 cylinder와 high-child/non-stutter branch를 닫는 전역 증명은 아니다.

1. RH: finite stress 대신 tail state certificate가 필요하다는 방향으로 이동했다. off-critical zero가 있으면 finite replayable positivity violation으로 내려온다는 stateful tail bridge는 아직 없다.
2. Collatz: `base_bits=12`, `adaptive_max_bits=22`, `max_chain_bits=96`에서 parent edge `113,115`개, open child edge `208,481`개를 검사했다. feature-stutter edge는 `56,714`개이고 비율은 `0.27203438`이다. 모든 stutter chain은 `signature_changed` `30,939`개 또는 `terminal` `25,775`개로 끝났고, unresolved는 `0`개였다. 최대 same-signature run은 `17`단계이다.
3. Goldbach: finite witness가 아니라 major/minor arc와 error budget을 상태 전이로 보존하는 cutoff ledger state machine이 필요하다.
4. Twin Prime: exact gap 2 mass가 parity countermodel 상태 전이에서 사라지지 않는 selector state machine이 필요하다.

Closed partial theorem:

```text
Every tested same-signature low-child stutter chain in the Ticket 32 Collatz bounded frontier exits the same local signature within the recorded finite budget. A certificate-carrying budget strictly decreases along repeated same-signature low-child stutter moves in this bounded frontier.
```

Refuted shortcut:

```text
The bounded stutter-budget certificate alone proves Collatz.
```

Reason:

```text
The budget is lookahead-derived and bounded to the tested frontier. A full proof still needs a theorem showing that every possible exact-cylinder path has finite budget or zero obstruction mass, and it must also close high-child and non-stutter transitions.
```

Remaining decisive target:

```text
CO-TICKET-33 GlobalMeasureCompactnessOrHighBranchClosure
```

### Ticket 33: Global measure pressure and high-branch obstruction

Generated artifact:

```text
data/open-problem/ticket33-global-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-33-global-tail-compactness.json
data/open-problem/collatz/co-ticket-33-global-measure-compactness.json
data/open-problem/goldbach/gb-ticket-33-global-cutoff-compactness.json
data/open-problem/twin-prime/tp-ticket-33-global-parity-compactness.json
```

Aggregate verdict:

```text
global_measure_open_no_resolution
```

한국어 요약: TICKET-33은 TICKET-32가 닫지 못한 high-child branch와 전역 compactness 문제를 직접 건드린다. Collatz exact-cylinder frontier를 `base_bits=12`에서 `max_bits=28`까지 level-by-level로 추적해 normalized open cylinder mass가 감소하는지 계산했다. 결과적으로 mass는 단조 감소했지만, 마지막 frontier mass는 양수이고 high-child branch도 계속 열려 있었다. 따라서 이것은 전역 증명이 아니라 “전역 measure theorem이 필요하다”는 정량적 증거이다.

1. RH: bounded tail certificate가 있어도 infinitely many zero contribution을 제어하는 global tail compactness theorem이 필요하다.
2. Collatz: open frontier mass는 `1.0`에서 `0.026959180832`까지 단조 감소했다. 마지막 frontier count는 `3,618,400`이다. 마지막 8개 level의 log2 mass fit은 per-bit factor `0.916768160879`를 보였다. 그러나 high-open child edge는 `3,901,346`개이고 high-only open child edge도 `125,449`개다. 즉 high branch가 자동으로 닫힌다는 shortcut은 반례를 갖는다.
3. Goldbach: finite cutoff ledger가 있어도 error term이 cutoff 이후 다시 열리지 않는 global cutoff compactness theorem이 필요하다.
4. Twin Prime: exact-gap selector가 있어도 parity state가 wider-gap leakage로 mass를 잃지 않는 global parity compactness theorem이 필요하다.

Closed partial theorem:

```text
In the tested Collatz adaptive frontier from 12 to 28 bits, normalized open cylinder mass decreases monotonically from 1.0 to 0.026959180832.
```

Refuted shortcut:

```text
High-child branches automatically close once low-child feature stutter is budgeted.
```

Reason:

```text
The tested frontier contains high-only open child edges: the low child can close while the high child remains open. Therefore high-branch closure requires its own theorem or automaton, not just the low-child stutter budget.
```

Remaining decisive target:

```text
CO-TICKET-34 HighBranchAutomatonOrMassLimitTheorem
```

Proof boundary:

```text
Finite monotone mass decrease and a negative fitted slope do not prove that open mass tends to zero. A full proof must establish a global compactness or mass-limit theorem for every future bit length, or a high-branch automaton that closes all remaining obstruction paths.
```

### Ticket 34: High-branch automaton and mass-limit split

Generated artifact:

```text
data/open-problem/ticket34-high-branch-automaton-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-34-tail-automaton-limit.json
data/open-problem/collatz/co-ticket-34-high-branch-automaton.json
data/open-problem/goldbach/gb-ticket-34-cutoff-automaton-limit.json
data/open-problem/twin-prime/tp-ticket-34-parity-automaton-limit.json
```

Aggregate verdict:

```text
high_branch_automaton_open_no_resolution
```

한국어 요약: TICKET-34는 TICKET-33에서 남은 high-branch obstruction을 둘로 분해했다. 첫째, finite automaton state만으로 high branch가 자동으로 닫히는지 검사했다. 둘째, pointwise closure가 실패한다면 aggregate mass contraction이 남는지 finite quotient의 spectral pressure를 계산했다. 결과는 둘 다 조심스럽다. 단순 finite-feature automaton은 state collision 때문에 막혔고, aggregate mass는 계속 줄어드는 압력이 보였지만 이것은 아직 `limsup < 1` 정리가 아니다.

1. RH: tail compactness는 tail automaton 또는 uniform zero-sum mass-limit theorem으로 분해된다. high-height surrogate zero 삽입에서 tail-kernel state collision을 검사해야 한다.
2. Collatz: `base_bits=12`에서 `max_bits=24`까지 high-branch automaton audit를 실행했다. transition parent는 `387,587`개였고, high-open parent는 `346,972`개, high-only parent는 `20,135`개였다. 모든 level의 aggregate open-mass ratio는 1보다 작았고 최대 ratio는 `0.944905286616`이었다. 그러나 both-open parent가 존재해 pointwise contraction은 막혔다.
3. Goldbach: cutoff compactness는 finite error-state automaton 또는 future error-state mass bound로 분해된다.
4. Twin Prime: parity compactness는 exact-gap mass가 wider-gap leakage로 사라지지 않는 automaton 또는 exact-gap mass-limit theorem으로 분해된다.

Finite automaton findings:

```text
coarse_debt: states=995, ambiguous=301, noncontracting=922, radius=0.675222044668
tail2_debt: states=6,532, ambiguous=1,722, noncontracting=5,963, radius=0.692640682511
tail4_debt: states=25,252, ambiguous=5,362, noncontracting=22,567, radius=0.685447084869
tail4_residue64: states=75,871, ambiguous=12,940, noncontracting=66,299, radius=0.674244169297
full_word_residue64: states=282,891, ambiguous=21,138, noncontracting=247,442, radius=0.533111158891
```

Closed partial theorem:

```text
In the tested Collatz frontier from 12 to 24 bits, every evaluated level has aggregate open-mass ratio below one.
```

Refuted shortcuts:

```text
A pointwise high-branch closure proof follows from low-child stutter budgets.
A small finite feature automaton can decide high-branch closure without state collisions.
```

Reason:

```text
The tested quotient families contain ambiguous states: the same finite state can map to different closure labels, including high-open and high-only outcomes. They also contain many pointwise noncontracting states with both children open. Therefore a proof cannot rely on these finite states alone.
```

Remaining decisive target:

```text
CO-TICKET-35 LimsupMassContractionOrStateRefinementTheorem
```

Proof boundary:

```text
Finite aggregate spectral radius below one is evidence for a mass-limit route, not a proof. A full Collatz proof still needs a symbolic theorem that the limsup of all future adaptive open-mass ratios is strictly below one, or a refined well-founded state that eliminates the observed collisions for every cylinder.
```

### Ticket 35: Limsup mass refinement and null-set gap

Generated artifact:

```text
data/open-problem/ticket35-limsup-mass-refinement-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-35-tail-nullset-exclusion.json
data/open-problem/collatz/co-ticket-35-limsup-mass-refinement.json
data/open-problem/goldbach/gb-ticket-35-exceptional-set-elimination.json
data/open-problem/twin-prime/tp-ticket-35-exact-gap-nullset.json
```

Aggregate verdict:

```text
limsup_mass_refinement_open_no_resolution
```

한국어 요약: TICKET-35는 지금까지의 결과를 버리지 않고 정리했다. TICKET-31은 local feature-only descent를 막았고, TICKET-32는 bounded low-child stutter budget을 만들었고, TICKET-33/34는 high branch와 aggregate mass contraction을 분리했다. 이번 결론은 더 엄격하다. Mass contraction은 중요한 신호지만, 그것만으로는 Collatz 증명이 아니다. 왜냐하면 measure-zero 예외 집합 안에도 개별 자연수 counterexample이 있을 수 있기 때문이다.

1. RH: finite-prefix나 measure-small tail failure가 아니라, 모든 off-critical zero를 uniform하게 배제하는 tail theorem이 필요하다.
2. Collatz: exact mass window `12..28 bits`에서 final open mass는 `0.026959180832`, max mass ratio는 `0.944905286616`, tail-window max ratio는 `0.935207747252`, finite candidate epsilon은 `0.064792252748`이다. 그러나 `mass_zero_not_pointwise_proof`가 핵심 장애물로 남았다.
3. Goldbach: almost-all positivity나 density evidence는 sparse exceptional even integer를 제거하지 못한다. pointwise cutoff theorem이 필요하다.
4. Twin Prime: bounded statistics나 typical exact-gap mass는 arbitrarily large exact gap-2 pairs를 강제하지 못한다. uniform exact-gap lower bound가 필요하다.

State refinement findings:

```text
full_word_residue64: blocked_by_state_collision, states=82,273, ambiguous=5,114, noncontracting=74,832
full_word_residue1024_bits_mod16: blocked_by_pointwise_noncontraction, states=113,645, ambiguous=0, noncontracting=99,229
full_word_residue4096_bits_mod32: blocked_by_pointwise_noncontraction, states=114,937, ambiguous=0, noncontracting=99,229
exact_residue_and_bits: collision_free_but_unbounded_identity_state, states=114,937, ambiguous=0, noncontracting=99,229
```

Discarded routes:

```text
mass-only Collatz proof without an arithmetic null-set exclusion theorem
fixed finite-feature automaton closure after observed state collisions
pointwise high-branch closure inherited from low-child stutter budgets
```

Retained routes:

```text
limsup mass contraction as a useful but insufficient global pressure statement
state refinement only if it becomes uniform and well-founded rather than identity-like
contrapositive search for an infinite natural-number path inside the null frontier
```

Closed partial theorem:

```text
The tested Collatz frontier keeps aggregate mass ratios below one through the recorded exact window.
```

Remaining decisive target:

```text
CO-TICKET-36 NullSetArithmeticExclusionOrUniformRankTheorem
```

Proof boundary:

```text
Even a proved measure-zero limiting obstruction set would not by itself prove Collatz for every positive integer. A full proof must either exclude natural-number paths from that null set, or provide a uniform well-founded rank that decreases on every infinite adaptive path.
```

### Ticket 36: Null-frontier arithmetic and pointwise exception exclusion

Generated artifact:

```text
data/open-problem/ticket36-null-frontier-arithmetic-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-36-offcritical-null-exclusion.json
data/open-problem/collatz/co-ticket-36-natural-null-frontier.json
data/open-problem/goldbach/gb-ticket-36-sparse-exception-exclusion.json
data/open-problem/twin-prime/tp-ticket-36-sparse-gap-exclusion.json
```

Aggregate verdict:

```text
null_frontier_arithmetic_open_no_resolution
```

한국어 요약: TICKET-36은 TICKET-35에서 남은 핵심 장애물인 `mass_zero_not_pointwise_proof`를 실제 산술 질문으로 바꿨다. 질량, 밀도, typical behavior가 아무리 좋아도 sparse/null exceptional object가 하나라도 무한히 남으면 난제는 깨진다. 따라서 네 난제 모두에서 필요한 것은 "예외가 드물다"가 아니라 "예외가 없다"는 pointwise theorem이다.

Collatz bounded natural-exit audit:

```text
tested odd n: 50,000 values, all odd n <= 100,000
base bits: 12
shallow probe: up to 96 bits
deep resolve: up to 180 bits
shallow unresolved count: 17
deep unresolved count: 0
max exit bits: 135
max exit slack over bit_length(n): 119
max exit minus odd Collatz steps: 27
direct sample termination: all tested direct orbits reached 1
```

Interpretation:

```text
Every tested odd integer exits the adaptive null frontier by 135 bits, so no bounded Collatz counterexample was found in the tested range. However, the audit refutes shallow natural-exclusion shortcuts: even n <= 100,000 can require much deeper certificate bits than its own bit length.
```

Discarded Collatz routes:

```text
measure-zero frontier proof without natural-integer exclusion
small constant slack theorem exit_bits <= bit_length(n) + C for C <= 112 in the tested range
stopping-time proxy proof unless stopping time is itself bounded by an independent rank
```

Retained Collatz routes:

```text
contrapositive search for a natural n with no frontier exit
uniform well-founded rank that implies finite frontier exit without using orbit termination as an oracle
deep arithmetic exclusion theorem for the limiting 2-adic null frontier
```

Cross-problem transfer:

1. RH: finite-window and measure-small tail tests are insufficient. A proof must exclude every off-critical zero pointwise.
2. Goldbach: almost-all positivity is insufficient. A zero-density infinite set of even exceptions would still falsify the conjecture.
3. Twin Prime: bounded prime statistics are insufficient. A proof must force exact gap 2 infinitely often, not merely bounded gaps or typical pair mass.
4. Collatz: mass decay is insufficient. A proof must exclude every positive integer from the limiting open frontier or give a non-circular decreasing rank.

Remaining decisive target:

```text
CO-TICKET-37 NaturalFrontierRankOrPointwiseExceptionElimination
```

Proof boundary:

```text
TICKET-36 does not prove or disprove any of the four open problems. It closes a methodological loophole: aggregate evidence is not enough. The next proof attempt must synthesize a pointwise rank/exclusion theorem, or deliberately search for a sparse/null counterexample object that survives all aggregate tests.
```

### Ticket 37: Pointwise rank synthesis and weak-rank counterexamples

Generated artifact:

```text
data/open-problem/ticket37-pointwise-rank-synthesis-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-37-pointwise-zero-rank.json
data/open-problem/collatz/co-ticket-37-pointwise-rank-synthesis.json
data/open-problem/goldbach/gb-ticket-37-pointwise-cutoff-rank.json
data/open-problem/twin-prime/tp-ticket-37-exact-gap-rank.json
```

Aggregate verdict:

```text
pointwise_rank_synthesis_open_no_resolution
```

한국어 요약: TICKET-37은 TICKET-36의 natural frontier exit audit을 rank synthesis 문제로 바꿨다. 즉, "모든 자연수가 언젠가 null frontier에서 빠져나간다"를 직접 증명하기 위해 `exit_bits`를 `bit_length(n)` 같은 비순환 양으로 제한할 수 있는지 시험했다. 약한 후보는 반례로 버리고, 아직 살아남은 후보는 증명 대상 정리로만 남겼다.

Collatz bounded rank audit:

```text
tested odd n: 2,500,000 values, all odd n <= 5,000,000
base bits: 12
max probe bits: 320
resolved count: 2,500,000
unresolved count: 0
max exit bits: 228
max exit ratio to bit_length(n): 12.0
max exit slack over bit_length(n): 206
```

Linear rank falsification:

```text
exit_bits <= 8 * bit_length(n): 61 violations
exit_bits <= 9 * bit_length(n): 14 violations
exit_bits <= 10 * bit_length(n): 9 violations
exit_bits <= 11 * bit_length(n): 3 violations
exit_bits <= 12 * bit_length(n): 0 violations in the bounded sample
```

Candidate retained, but not proved:

```text
n >= 128 implies exit_bits <= 11 * bit_length(n); all tested n imply exit_bits <= 12 * bit_length(n)
```

Interpretation:

```text
This is a stronger and more useful target than raw mass decay: it is a pointwise-looking rank statement. But it is still bounded evidence. A proof needs a symbolic extension lemma showing that unseen adaptive frontier states cannot exceed the same piecewise linear rank.
```

Discarded Collatz routes:

```text
exit_bits <= 8 * bit_length(n) as a global rank
exit_bits <= 9 * bit_length(n) as a global rank
exit_bits <= 10 * bit_length(n) as a global rank
unqualified exit_bits <= 11 * bit_length(n) without finite seed handling
```

Retained Collatz routes:

```text
finite seed set plus exit_bits <= 11 * bit_length(n) for n >= 128 as a bounded theorem candidate
global exit_bits <= 12 * bit_length(n) as a weaker bounded theorem candidate
symbolic extension lemma over adaptive frontier states
```

Cross-problem transfer:

1. RH: a pointwise zero-exclusion rank is needed; finite-height verification and smoothed averages remain support only.
2. Goldbach: a pointwise even-cutoff rank is needed; density positivity cannot exclude a sparse exceptional set.
3. Twin Prime: an exact-gap-2 rank is needed; bounded-gap mass must not leak into wider gaps.
4. Collatz: a frontier-exit rank is needed; the bounded candidate is now concrete but still lacks the infinite extension theorem.

Remaining decisive target:

```text
CO-TICKET-38 SymbolicFrontierExtensionLemma
```

Proof boundary:

```text
TICKET-37 does not prove or disprove any of the four open problems. It improves the search by producing bounded counterexamples to weak rank candidates and by naming a sharper surviving theorem target. The next step is not more finite checking alone; it is a symbolic extension lemma or a new counterexample family that breaks the surviving rank.
```

### Ticket 38: Symbolic frontier extension and shortcut rejection

Generated artifact:

```text
data/open-problem/ticket38-symbolic-frontier-extension-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-38-symbolic-zero-extension.json
data/open-problem/collatz/co-ticket-38-symbolic-frontier-extension.json
data/open-problem/goldbach/gb-ticket-38-symbolic-cutoff-extension.json
data/open-problem/twin-prime/tp-ticket-38-symbolic-gap-extension.json
```

Aggregate verdict:

```text
symbolic_frontier_extension_open_no_resolution
```

한국어 요약: TICKET-38은 TICKET-37에서 살아남은 “점별 rank” 후보를 실제 증명으로 끌어올리기 위해 필요한 symbolic extension lemma를 직접 공격했다. 결론은 중요하지만 부정적이다. 고정된 비트 윈도우 안에서 모든 open frontier가 닫힌다는 단순 보조정리와, 하나의 scalar debt 함수가 모든 open edge에서 엄격히 감소한다는 보조정리는 bounded symbolic graph에서 반례성 edge를 대량으로 만들며 실패했다. 따라서 다음 증명 시도는 더 많은 finite checking이 아니라 phase/state-dependent potential 또는 명시적 surviving frontier family 분석이어야 한다.

Collatz symbolic frontier audit:

```text
frontier bits: 12..24
open edge count: 704,456
final frontier count: 317,095
max survival ratio: 0.944905286616
```

Scalar debt falsification:

```text
lambda = 1.45: 427,227 nondecreasing open edges
lambda = 1.50: 452,949 nondecreasing open edges
lambda = log2(3): 452,949 nondecreasing open edges
lambda = 1.60: 452,949 nondecreasing open edges
lambda = 1.70: 452,949 nondecreasing open edges
```

Discarded Collatz routes:

```text
bounded local closure from 12 bits to a fixed later bit depth
single scalar debt potential as a strict descent proof
aggregate mass contraction treated as a pointwise rank extension theorem
```

Retained Collatz routes:

```text
finite seed handling for stutter-like residues
phase/state-dependent potential instead of scalar debt alone
symbolic extension lemma combining aggregate contraction with pointwise rank
```

Cross-problem transfer:

1. RH: finite-height zero checks and averaged pressure are not enough. A proof needs a symbolic zero-exclusion certificate that rejects every hypothetical off-critical configuration.
2. Goldbach: almost-all or averaged representation pressure is not enough. A proof needs a stateful lower-bound certificate that remains positive for every even integer beyond a finite seed interval.
3. Twin Prime: bounded-gap pressure is not enough. A proof needs an exact-gap selector that prevents gap-2 mass from leaking into wider admissible gaps.
4. Collatz: aggregate mass decay and scalar debt are not enough. A proof needs a phase/state extension theorem or an explicit infinite counterexample object.

Remaining decisive target:

```text
CO-TICKET-39 PhaseStatePotentialSynthesis
```

Proof boundary:

```text
TICKET-38 does not prove or disprove any of the four open problems. It removes three tempting but false proof shortcuts and narrows the next viable proof attempt to a stateful symbolic extension lemma. A future proof must either synthesize a verified phase/state potential with no nondecreasing open cycle, or construct a coherent infinite survivor/counterexample object.
```

### Ticket 39: Phase/state potential synthesis

Generated artifact:

```text
data/open-problem/ticket39-phase-state-potential-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-39-phase-state-zero-potential.json
data/open-problem/collatz/co-ticket-39-phase-state-potential.json
data/open-problem/goldbach/gb-ticket-39-state-cone-potential.json
data/open-problem/twin-prime/tp-ticket-39-gap-leakage-potential.json
```

Aggregate verdict:

```text
phase_state_potential_open_no_resolution
```

한국어 요약: TICKET-39는 TICKET-38에서 실패한 scalar debt 방식을 버리고, phase/state quotient 위에서 실제 rank 후보를 합성했다. 거친 상태공간은 cycle이 남아서 폐기되었고, `phase_mod16_tail4_residue256` 상태공간은 finite window에서 DAG가 되어 topological rank를 갖는다. 더 긴 28비트 phase-wrap probe에서도 같은 후보는 sampled cycle 없이 유지되었다. 하지만 이것은 아직 Collatz 증명이 아니다. 빠진 정리는 “앞으로 나타날 모든 reachable state transition도 이 DAG 순서를 벗어나지 않는다”는 transition-closure theorem이다.

Collatz primary phase/state audit:

```text
frontier bits: 12..24
open edge count: 704,456
final frontier count: 317,095
```

State-family comparison:

```text
phase_mod4_tail2_debt: cycle detected, cyclic core 16,245 nodes
phase_mod8_tail4_residue64: cycle detected, cyclic core 63,270 nodes
phase_mod16_tail4_residue256: finite DAG candidate, max topological rank 12, edge violations 0
phase_mod32_tail6_residue1024: finite DAG candidate, max topological rank 12, edge violations 0
identity_residue_bits: acyclic but identity-like and not a uniform proof object
```

Deep phase-wrap probe:

```text
family: phase_mod16_tail4_residue256
frontier bits: 12..28
open edge count: 7,960,722
final frontier count: 3,618,400
status: phase_wrapped_finite_dag_candidate
max topological rank: 16
rank edge violations: 0
```

Discarded Collatz routes:

```text
coarse phase/state quotient after a quotient cycle is detected
identity-like residue+bits state as a uniform proof object
finite-window DAG rank treated as a Collatz proof without future transition closure
```

Retained Collatz routes:

```text
phase_mod16_tail4_residue256 quotient as the current finite theorem candidate
transition-closure theorem for every future reachable phase/state edge
contrapositive search for a future wrap-around cycle or coherent infinite survivor state
```

Cross-problem transfer:

1. RH: replace scalar or averaged zero pressure with a closed finite zero-configuration quotient and positivity rank.
2. Goldbach: replace averaged representation margins with a finite error-cone quotient that keeps each even integer pointwise positive.
3. Twin Prime: replace bounded-gap pressure with an exact-gap leakage quotient that prevents mass from escaping into wider admissible gaps.
4. Collatz: replace scalar debt with a concrete phase/state DAG candidate, then prove closure or find a future state cycle.

Remaining decisive target:

```text
CO-TICKET-40 PhaseStateTransitionClosureOrCycleCounterexample
```

Proof boundary:

```text
TICKET-39 does not prove or disprove any of the four open problems. It is a stronger synthesis step than TICKET-38 because it produces a concrete finite rank candidate and separately rejects coarse cyclic quotients. The next step must either prove symbolic closure of the phase_mod16_tail4_residue256 transition system or find a reachable future cycle/counterexample state that defeats it.
```

### Ticket 40: Transition closure or cycle counterexample

Generated artifact:

```text
data/open-problem/ticket40-transition-closure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-40-zero-transition-closure.json
data/open-problem/collatz/co-ticket-40-transition-closure.json
data/open-problem/goldbach/gb-ticket-40-error-cone-transition-closure.json
data/open-problem/twin-prime/tp-ticket-40-gap-leakage-transition-closure.json
```

Aggregate verdict:

```text
transition_closure_open_no_resolution
```

한국어 요약: TICKET-40은 TICKET-39의 좋은 후보를 그대로 이어받아 “정말 닫힌 전이 정리로 승격 가능한가?”를 공격했다. 결과적으로 `phase_mod16_tail4_residue256` 상태가 branching label 자체는 안정적으로 결정하지만, exact child-state signature는 같은 parent state에서도 여러 방식으로 갈라진다. 따라서 deterministic finite transducer 방식의 증명은 버린다. 그러나 sampled nondeterministic transition relation은 26비트 extension probe까지 cycle 없이 유지되고 topological rank violation도 없었다. 그래서 남은 증명 목표는 결정적 전이가 아니라, 전역적으로 닫힌 비결정적 well-founded relation을 증명하거나 미래 reachable cycle을 찾아 반례 후보를 만드는 것이다.

Collatz primary closure audit:

```text
frontier bits: 12..24
parent instance count: 389,409
state count: 188,651
state edge count: 440,614
ambiguous label states: 0
ambiguous child-signature states: 39,077
max child signatures for one state: 34
deterministic exact-child closure: refuted_by_child_state_signature_collision
```

Collatz extension probe:

```text
frontier bits: 12..26
parent instance count: 1,294,925
state count: 413,343
state edge count: 1,340,093
final frontier count: 1,099,648
ambiguous label states: 0
ambiguous child-signature states: 97,019
sampled cycle detected: false
max topological rank: 14
rank edge violations: 0
```

Discarded Collatz routes:

```text
deterministic exact-child finite transducer for phase_mod16_tail4_residue256
finite-window acyclic rank treated as a global Collatz proof
state quotients that do not state how all future reachable transitions are closed
```

Retained Collatz routes:

```text
label-level closure as a possible symbolic lemma, not yet a theorem
nondeterministic acyclic transition relation with sampled topological rank
contrapositive search for a future reachable cycle or escaping survivor state
```

Cross-problem transfer:

1. RH: split a zero-exclusion route into deterministic zero-state closure, nondeterministic positivity-state rank, and explicit off-critical zero/cycle counterexample targets.
2. Goldbach: split an error-cone route into deterministic error update rejection, nondeterministic pointwise positivity rank, and exceptional even-integer counterexample search.
3. Twin Prime: split an exact-gap route into deterministic leakage rejection, nondeterministic exact-gap residual rank, and last-twin absorbing-cycle search.
4. Collatz: reject deterministic child-state closure while retaining a nondeterministic acyclic rank candidate.

Remaining decisive target:

```text
CO-TICKET-41 SymbolicNondeterministicClosureOrReachableCycle
```

Proof boundary:

```text
TICKET-40 does not prove or disprove any of the four open problems. It is useful because it removes a specific false promotion path: a finite sampled rank cannot be treated as a deterministic closed transducer. The next step must either prove symbolic closure of the nondeterministic transition relation or find a reachable future cycle/counterexample state.
```

### Ticket 41: Rank escape normalization

Generated artifact:

```text
data/open-problem/ticket41-rank-escape-normalization-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-41-parametric-zero-state-normalization.json
data/open-problem/collatz/co-ticket-41-rank-escape-normalization.json
data/open-problem/goldbach/gb-ticket-41-parametric-error-cone-normalization.json
data/open-problem/twin-prime/tp-ticket-41-parametric-gap-leakage-normalization.json
```

Aggregate verdict:

```text
rank_escape_normalization_open_no_resolution
```

한국어 요약: TICKET-41은 TICKET-40의 남은 길을 더 정밀하게 검토했다. 핵심 수정은 `phase_mod16_tail4_residue256`를 전역 finite quotient처럼 부르면 안 된다는 점이다. 이 state에는 `prefix_length`, `consumed_bits`, `rounded_debt` 같은 성장 좌표가 들어가므로 horizon을 늘리면 새 좌표와 새 edge가 계속 생긴다. 따라서 고정된 finite-window DAG는 증명 객체가 될 수 없다. 남는 길은 더 큰 계산이 아니라, 성장 좌표를 포함하는 parametric symbolic transition schema와 well-founded measure를 증명하거나, 그 schema 안에서 nondecreasing cycle 또는 escaping coordinate ray를 찾는 것이다.

Collatz snapshots:

```text
12..24: nodes 282,660, edges 440,614, sinks 101,810, distinct coordinates 1,197, max rank 12
12..25: nodes 413,343, edges 688,432, sinks 145,873, distinct coordinates 1,347, max rank 13
12..26: nodes 590,519, edges 1,049,993, sinks 197,544, distinct coordinates 1,524, max rank 14
```

Fixed-relation escape:

```text
24 -> 25: new edges 247,818, reopened previous sinks 86,620, new coordinates 150
25 -> 26: new edges 361,561, reopened previous sinks 125,505, new coordinates 177
24 -> 26 total distinct coordinate delta: 327
```

Discarded Collatz routes:

```text
fixed finite-window DAG as a global proof object
phase_mod16_tail4_residue256 described as a global finite quotient
rank values computed on a horizon before checking future sink reopening
```

Retained Collatz routes:

```text
parametric symbolic transition schema over phase, tail, residue, and growth coordinates
well-founded ordinal or lexicographic measure that can absorb coordinate growth
counterexample search for reachable cycles, reopened sinks, or escaping coordinate rays
```

Cross-problem transfer:

1. RH: a finite-height zero-state graph must be replaced by a parametric zero-configuration normalization theorem.
2. Goldbach: a finite cutoff error-cone graph must be replaced by a parametric error-cone transition theorem for all large even integers.
3. Twin Prime: a finite exact-gap leakage graph must be replaced by a scale-parametric exact-gap residual theorem.
4. Collatz: a fixed sampled DAG must be replaced by symbolic templates plus a well-founded measure, or by an explicit escaping ray/cycle.

Remaining decisive target:

```text
CO-TICKET-42 ParametricTransitionTemplateOrNondecreasingCycle
```

Proof boundary:

```text
TICKET-41 does not prove or disprove any of the four open problems. It corrects a finite-quotient overstatement and gives a concrete counterexample to fixed finite-window closure. A future proof must normalize the growing coordinates symbolically, while a future disproof route would be a reachable nondecreasing cycle or escaping coordinate ray inside that normalized system.
```

### Ticket 42: Parametric transition template lab

Generated artifact:

```text
data/open-problem/ticket42-parametric-transition-template-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-42-parametric-zero-template.json
data/open-problem/collatz/co-ticket-42-parametric-transition-template.json
data/open-problem/goldbach/gb-ticket-42-parametric-error-template.json
data/open-problem/twin-prime/tp-ticket-42-parametric-gap-template.json
```

Aggregate verdict:

```text
parametric_template_open_no_resolution
```

한국어 요약: TICKET-42는 TICKET-41에서 남긴 숙제인 parametric transition schema를 실제로 만들기 시작한 단계다. 고정된 finite-window graph 대신 `phase`, valuation tail, residue, next valuation을 template node로 두고, `prefix_length`, `consumed_bits`, debt를 성장 좌표로 따로 기록했다. 중요한 결과는 예상과 달리 26-bit 표본에서 template cycle을 찾지 못했다는 점이다. 이것은 proof route를 살리는 좋은 신호지만, 증명은 아니다. 이유는 같은 template edge가 서로 다른 `delta_prefix`, `delta_consumed`, `delta_debt`를 가질 수 있기 때문이다. 따라서 다음 증명 의무는 bounded acyclicity가 아니라, template edge가 어떤 큰 cylinder에서 실제로 lift되는지와 그때 성장 좌표가 항상 well-founded measure를 감소시키는지 증명하는 것이다.

Collatz template families:

```text
phase16_tail2_residue64_v8: nodes 14,357, edges 126,994, ambiguous template edges 8,218, sampled cycles 0
phase16_tail3_residue128_v12: nodes 59,388, edges 352,790, ambiguous template edges 6,887, sampled cycles 0
phase16_tail4_residue256_v16: nodes 165,812, edges 710,227, ambiguous template edges 5,393, sampled cycles 0
phase16_tail4_residue256_vexact: nodes 165,841, edges 710,241, ambiguous template edges 5,393, sampled cycles 0
```

Raw frontier pressure:

```text
raw open edges processed: 2,392,525
raw nondecreasing debt edges: 1,510,781
sampled template cycle status: no_sampled_template_cycle_found_through_26_bits
total ambiguous template edge count across families: 25,891
```

Parametric update schema:

```text
phase' = phase + 1 mod 16
prefix_length' = prefix_length + delta_prefix
consumed_bits' = consumed_bits + delta_consumed
debt' = debt + delta_prefix * log2(3) - delta_consumed
tail' = suffix(tail plus newly consumed valuation word)
```

Discarded Collatz routes:

```text
absence of sampled template cycles treated as a Collatz proof
template cycle interpreted directly as a Collatz counterexample without a compatible lift
finite template edge treated as deterministic without delta guards for prefix, consumed bits, and debt
larger bounded horizon treated as a substitute for parametric lift closure
```

Retained Collatz routes:

```text
parametric transition schema with prefix_length, consumed_bits, and debt deltas
cycle-lift search for a compatible infinite nondecreasing template ray
well-founded measure that uses growth coordinates, not only the finite template node
```

Interpretation:

1. The sampled template graph did not refute the proof route through 26 bits.
2. The sampled graph also does not prove Collatz, because future lift closure is still missing.
3. Ambiguous coordinate deltas show why a finite template node alone is not a deterministic transition theorem.
4. A real counterexample route would need a compatible infinite lift of a nondecreasing cycle, not only a quotient cycle.

Remaining decisive target:

```text
CO-TICKET-43 LiftConstraintSolverOrWellFoundedMeasure
```

Proof boundary:

```text
TICKET-42 does not prove or disprove any of the four open problems. It preserves a promising bounded template-rank route because no sampled template cycle was found, but it rejects the shortcut from bounded acyclicity to truth. A proof now needs parametric lift closure plus a well-founded growth-coordinate measure; a disproof route needs a compatible infinite lift of a nondecreasing cycle.
```

### Ticket 43: Lift constraint and measure lab

Generated artifact:

```text
data/open-problem/ticket43-lift-constraint-measure-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-43-zero-lift-measure.json
data/open-problem/collatz/co-ticket-43-lift-constraint-measure.json
data/open-problem/goldbach/gb-ticket-43-error-lift-measure.json
data/open-problem/twin-prime/tp-ticket-43-gap-lift-measure.json
```

Aggregate verdict:

```text
lift_constraint_measure_open_no_resolution
```

한국어 요약: TICKET-43은 TICKET-42의 약점을 직접 고친다. TICKET-42에서는 26-bit 표본에서 template cycle이 없었기 때문에 "best cycle을 lift한다"는 다음 단계가 논리적으로 맞지 않았다. TICKET-43은 방향을 바꿔, `M(template, debt) = scale * topological_rank(template) + debt` 형태의 bounded measure가 실제 샘플 template edge에서 감소하는지 검사하고, 그 측도가 horizon 확장에서도 닫히는지를 확인한다.

Collatz lift snapshots:

```text
24 bits: nodes 97,806, edges 322,907, max rank 12, scale 11, min margin 0.584962500721
25 bits: nodes 128,371, edges 480,873, max rank 13, scale 11, min margin 0.584962500721
26 bits: nodes 165,841, edges 710,241, max rank 14, scale 11, min margin 0.584962500721
```

Important bounded result:

```text
sampled measure status: sampled_measure_decreases_on_all_template_edges
candidate: M(template, debt) = scale * topological_rank(template) + debt
scale: 11
minimum sampled margin: 0.584962500721
invalid rank-gap edges: 0
```

Important obstruction:

```text
24 -> 25: new template edges 157,966, previous ranks changed 94,080, old-measure unknown-rank edges 157,966
25 -> 26: new template edges 229,368, previous ranks changed 124,027, old-measure unknown-rank edges 229,368
closure status: rank_lift_not_closed_under_horizon_extension
```

Interpretation:

1. The debt-only route is refuted as a proof strategy because many raw edges have nondecreasing debt.
2. A stronger bounded certificate exists in the sampled graph: `scale * rank + debt` decreases on every sampled template edge through 26 bits.
3. This is still not a Collatz proof, because the rank is recomputed when the horizon grows; 25 -> 26 changes 124,027 previous-node ranks and introduces 229,368 new template edges whose ranks were unknown to the old measure.
4. The next theorem is therefore a lift-closure theorem: every future cylinder lift must preserve the template relation and a horizon-independent well-founded measure, or the search must find a future edge that violates all finite-rank extensions.

English summary: TICKET-43 upgrades the Collatz track from finite acyclicity to finite measure synthesis. The sampled measure is a real bounded certificate, not a proof. The remaining infinite obligation is to replace horizon-specific topological rank with a lift-stable rank or another well-founded measure whose decrease can be proved for every future cylinder lift.

Remaining decisive target:

```text
CO-TICKET-44 HorizonIndependentLiftRankOrCounteredge
```

Proof boundary:

```text
TICKET-43 does not prove or disprove any of the four open problems. It improves the proof attempt by producing a bounded decreasing measure, and it improves the counterexample attempt by identifying exactly where future lift edges could break finite-rank extensions.
```

### Ticket 44: Feature-measure counteredge lab

Generated artifact:

```text
data/open-problem/ticket44-feature-measure-counteredge-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-44-zero-feature-counteredge.json
data/open-problem/collatz/co-ticket-44-feature-measure-counteredge.json
data/open-problem/goldbach/gb-ticket-44-margin-feature-counteredge.json
data/open-problem/twin-prime/tp-ticket-44-gap-feature-counteredge.json
```

Aggregate verdict:

```text
feature_measure_counteredge_open_no_resolution
```

한국어 요약: TICKET-44는 TICKET-43에서 남은 가장 위험한 논리적 틈을 공격한다. TICKET-43의 `scale * sampled_rank + debt` 측도는 26-bit 표본에서는 모든 template edge에서 감소하지만, 그 rank는 horizon을 늘릴 때 다시 계산된다. 따라서 이것을 무한 증명으로 승격하려면 horizon에 의존하지 않는 명시적 feature measure가 필요하다. TICKET-44는 여러 feature family를 제안하고, 각 family가 실제 edge에서 감소 측도로 작동하는지 counterexample-guided 방식으로 검사했다. 결과적으로 `debt_only_constant`는 390,494개의 zero-delta refuter로 정확히 반박되었다. 더 풍부한 feature family들은 bounded affine search에서 인증되지 않았지만, 이것은 불가능성 증명이 아니라 현재 feature와 solver의 한계다. 살아남은 방향은 explicit counteredge extraction과 horizon-independent symbolic rank theorem이다.

English summary: TICKET-44 attacks the remaining promotion gap in TICKET-43. A sampled rank table is a useful bounded certificate, but it is not an invariant proof object if the rank changes under horizon extension. TICKET-44 therefore searches for explicit horizon-independent feature measures and records exact counteredges when a candidate family cannot work. The debt-only control is exactly refuted; richer compact affine feature families remain uncertified rather than impossible. This narrows the proof route to a symbolic rank or measure whose decrease is stable under every future cylinder lift.

Collatz feature-measure audit:

```text
template family: phase16_tail4_residue256_vexact
max bits: 26
template nodes: 165,841
template edges: 710,241
raw open edges processed: 2,392,525
exactly refuted feature families: 1
not certified or still open feature families: 4
```

Feature trial summary:

```text
debt_only_constant:
  status: exact_zero_delta_counteredge_refutes_feature_measure
  feature dimension: 1
  unique constraints: 1
  positive-debt pressure edges: 390,494
  zero-delta refuters: 390,494
  affine violations: 1

phase_tail_scalar:
  status: not_certified_by_bounded_affine_search
  feature dimension: 7
  unique constraints: 4,748
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 2,608

numeric_template_coordinates:
  status: not_certified_by_bounded_affine_search
  feature dimension: 7
  unique constraints: 23,067
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 12,290

residue_binary_coordinates:
  status: not_certified_by_bounded_affine_search
  feature dimension: 14
  unique constraints: 23,067
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 12,290

phase_residue_onehot_tail_numeric:
  status: not_certified_by_bounded_affine_search
  feature dimension: 37
  unique constraints: 74,629
  positive-debt pressure edges: 390,494
  zero-delta refuters: 0
  affine violations: 1,126
```

Preserved TICKET-43 baseline:

```text
sampled rank-debt measure: sampled_measure_decreases_on_all_template_edges
scale: 11
minimum sampled margin: 0.584962500721
invalid rank-gap edges: 0
```

Horizon-extension obstruction:

```text
25 -> 26 new template edges: 229,368
25 -> 26 changed previous-node ranks: 124,027
25 -> 26 old-measure unknown-rank edges: 229,368
closure status: rank_lift_not_closed_under_horizon_extension
```

Discarded Collatz routes:

```text
debt-only descent as a proof measure
observed-node rank table treated as a horizon-independent theorem
bounded affine feature search treated as an impossibility proof for richer nonlinear measures
```

Retained Collatz routes:

```text
exact counteredge extraction for every proposed feature family
horizon-independent symbolic rank or ordinal-valued measure
future-lift theorem proving that every cylinder edge preserves the symbolic decrease
```

Cross-problem transfer:

1. RH: a zero-exclusion feature score must survive exact off-critical zero-lift counteredge extraction before it can be promoted to a positive-kernel theorem.
2. Goldbach: an error-margin feature score must survive exceptional-residue counteredges before it can be promoted to an explicit positivity theorem.
3. Twin Prime: an exact-gap feature score must survive leakage counteredges before it can be promoted to an infinite bounded-gap theorem.
4. Collatz: a finite rank table must be replaced by a symbolic rank or measure, or by a future edge that violates every proposed symbolic measure.

Remaining decisive target:

```text
CO-TICKET-45 SymbolicRankClauseOrFutureCounteredge
```

Proof boundary:

```text
TICKET-44 does not prove or disprove any of the four open problems. It improves the proof attempt by exactly refuting weak horizon-independent measures, preserving the bounded rank-table certificate only as evidence, and isolating the next proof obligation: a symbolic, horizon-stable rank or an explicit future counteredge against it.
```

### Ticket 45: Symbolic rank clause lab

Generated artifact:

```text
data/open-problem/ticket45-symbolic-rank-clause-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-45-symbolic-zero-clause.json
data/open-problem/collatz/co-ticket-45-symbolic-rank-clause.json
data/open-problem/goldbach/gb-ticket-45-symbolic-margin-clause.json
data/open-problem/twin-prime/tp-ticket-45-symbolic-gap-clause.json
```

Aggregate verdict:

```text
symbolic_rank_clause_open_no_resolution
```

한국어 요약: TICKET-45는 TICKET-44에서 남은 목표인 `horizon-independent symbolic rank`를 실제로 압박한다. 핵심 아이디어는 상태들을 symbolic clause로 묶고, nonnegative-debt pressure edge가 같은 clause 안에서 돌거나 pressure graph에 cycle을 만들면 그 clause family는 어떤 scalar rank를 주어도 증명 측도가 될 수 없다는 것이다. 가장 중요한 발견은 `phase_only`가 26-bit와 27-bit에서는 scale 11로 통과하지만, 28-bit에서 phase `11 -> 12` edge가 추가되면서 modulo-16 pressure cycle이 닫힌다는 점이다. 따라서 phase-only rank는 좋은 후보처럼 보이다가 미래 horizon에서 정확히 폐기된다. 이것은 Collatz 반례가 아니라 phase-only 증명 전략의 반례다.

English summary: TICKET-45 turns the remaining symbolic-rank obligation into a counterexample-guided clause test. A symbolic clause family is rejected when nonnegative-pressure edges force a same-clause loop or a pressure cycle. The phase-only family is especially useful as a diagnostic: it passes through 26 and 27 bits, then fails at 28 bits when a new `11 -> 12` pressure edge closes the phase cycle. This refutes the phase-only proof route, not Collatz.

Collatz symbolic-clause audit:

```text
26-bit template nodes: 165,841
26-bit template edges: 710,241
raw open edges processed: 2,392,525
26-bit exactly refuted clause families: 0
future-wrap refuted clause families: 1
sampled clause candidates through 26 bits: 1
```

Clause trial summary at 26 bits:

```text
phase_only:
  status: sampled_symbolic_clause_rank_found_not_proof
  clauses: 15
  pressure clause edges: 14
  selected scale: 11
  minimum sampled margin: 0.584962500721

phase_tail_mass_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 2,413
  pressure clause edges: 25,530

phase_tail_residue16_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 46,885
  pressure clause edges: 149,685

phase_tail_residue64_vbucket:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 90,008
  pressure clause edges: 248,120

phase_tail_residue256_vexact:
  status: not_certified_by_symbolic_clause_scale_interval
  clauses: 165,841
  pressure clause edges: 390,494
```

Phase-wrap counteredge:

```text
probe: 27 -> 28 bits
status: pressure_cycle_counterexample_refutes_clause_rank
new pressure clause edge: [11] -> [12]
max delta debt: 7.415037499279
edge count represented by this clause edge: 3,618,400
example parent template: [11,[1,1,1,9],191,1]
example child template: [12,[1,1,1,1],191,12]
```

Interpretation:

1. The phase-only rank looked promising because the observed phase chain had not wrapped yet.
2. Once the 28-bit horizon exposes the `11 -> 12` pressure edge, phase-only rank would require a strict decrease around a full modulo-16 cycle, which is impossible.
3. Richer finite clause families were not certified by the current pressure-rank interval. This is not an impossibility proof for every nonlinear or ordinal-valued measure.
4. The observed exact-template rank remains a bounded ceiling certificate, but its clause and pressure-edge sets change under horizon extension.

Discarded Collatz routes:

```text
phase-only rank as a Collatz proof measure
coarse symbolic quotients promoted before phase-wrap testing
observed exact-template rank table treated as an infinite theorem
```

Retained Collatz routes:

```text
pressure-cycle extraction for proposed symbolic clauses
stable symbolic family whose pressure graph remains acyclic under future lifts
parametric clause grammar plus a proof that every future lifted edge keeps a nonempty scale interval
```

Cross-problem transfer:

1. RH: a symbolic zero-clause grammar must survive off-critical pressure-cycle extraction before it can become a zero-free theorem.
2. Goldbach: a symbolic margin-clause grammar must survive exceptional-residue pressure cycles before it can become a positivity theorem.
3. Twin Prime: a symbolic exact-gap grammar must survive leakage pressure cycles before it can become an exact gap-2 lower-bound theorem.
4. Collatz: any low-dimensional symbolic rank must be tested not only at the current horizon but also at the first horizon where its quotient cycles can close.

Remaining decisive target:

```text
CO-TICKET-46 StableClauseGrammarOr27PlusCounteredge
```

Proof boundary:

```text
TICKET-45 does not prove or disprove any of the four open problems. It improves the proof attempt by finding a concrete future-horizon counteredge against the tempting phase-only symbolic rank, and it improves the search protocol by requiring every proposed symbolic clause grammar to survive pressure-cycle extraction before formal promotion.
```

### Ticket 46: Stable clause grammar lab

Generated artifact:

```text
data/open-problem/ticket46-stable-clause-grammar-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-46-stable-zero-grammar.json
data/open-problem/collatz/co-ticket-46-stable-clause-grammar.json
data/open-problem/goldbach/gb-ticket-46-stable-margin-grammar.json
data/open-problem/twin-prime/tp-ticket-46-stable-gap-grammar.json
```

Aggregate verdict:

```text
stable_clause_grammar_restricted_no_go_open_no_resolution
```

한국어 요약: TICKET-46은 TICKET-45에서 남은 질문을 더 강하게 압박한다. TICKET-45는 `phase_only`가 28-bit에서 깨진다는 것을 보였지만, 더 정교한 clause grammar들이 28-bit wrap 이후에도 버틸 수 있는지는 남아 있었다. TICKET-46은 같은 28-bit horizon에서 다섯 family 모두를 다시 검사했고, `phase_only`, `phase_tail_mass_vbucket`, `phase_tail_residue16_vbucket`, `phase_tail_residue64_vbucket`, `phase_tail_residue256_vexact` 전부가 nonnegative-pressure cycle을 갖는다는 결과를 얻었다. 따라서 이 다섯 종류의 finite template-local scalar clause-rank 증명 전략은 제한된 의미에서 모두 폐기된다. 이것은 Collatz의 반례도 아니고 Collatz 증명도 아니다. 정확한 결론은 “현재 테스트한 scalar clause-rank proof route는 더 이상 남아 있지 않다”이다.

English summary: TICKET-46 strengthens the TICKET-45 obstruction. TICKET-45 showed that the phase-only rank fails at the first visible modulo-16 wrap. TICKET-46 reruns the clause-rank stress test at the same 28-bit horizon for all five TICKET45 families. Every tested finite template-local scalar clause grammar becomes pressure-cyclic, including the exact observed-template table. This is a restricted no-go theorem for those proof routes, not a proof or disproof of Collatz.

Collatz stable-clause audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
raw open edges processed: 7,960,722
tested clause families: 5
28-bit refuted clause families: 5
28-bit stable clause families: 0
```

28-bit stress result:

```text
phase_only:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 16
  pressure clause edges: 16
  new pressure edges from 27->28: 1

phase_tail_mass_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 2,960
  pressure clause edges: 37,948
  new pressure edges from 27->28: 6,042

phase_tail_residue16_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 70,498
  pressure clause edges: 261,971
  new pressure edges from 27->28: 58,393

phase_tail_residue64_vbucket:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 138,390
  pressure clause edges: 448,510
  new pressure edges from 27->28: 105,553

phase_tail_residue256_vexact:
  status: pressure_cycle_counterexample_refutes_clause_rank
  clauses: 261,367
  pressure clause edges: 741,372
  new pressure edges from 27->28: 187,086
```

First shared phase-wrap pressure edge:

```text
edge: [11] -> [12]
max delta debt: 7.415037499279
edge count represented in phase-only quotient: 3,618,400
example parent template: [11,[1,1,1,9],191,1]
example child template: [12,[1,1,1,1],191,12]
```

Escape-coordinate audit:

1. `unwrapped_phase_epoch`: 현재 template key에는 phase modulo 16만 있으므로, unwrapped epoch는 외부 lift depth나 path history를 끌어온다. 이 좌표는 아직 finite horizon-independent grammar가 아니다.
2. `depth_or_max_bits_bucket`: bounded horizon을 기억하면 cycle을 깨는 것처럼 보일 수 있지만, 29-bit, 30-bit로 늘릴 때 다시 커지는 좌표라면 증명 객체가 아니다.
3. `exact_observed_template_table`: 26-bit에서는 bounded ceiling certificate였지만, 28-bit에서는 새 clause와 pressure edge가 대량으로 추가되고 pressure graph도 cyclic이 된다.

Discarded Collatz routes:

```text
phase-only scalar clause rank
coarse tail-mass scalar clause rank
low-residue scalar clause rank
exact observed-template scalar clause rank treated as an infinite theorem
horizon-depth or max_bits escape coordinate promoted before a well-founded theorem is proved
```

Retained Collatz routes:

```text
ordinal-valued or stateful measure with a template-local update rule
explicit 29-bit/30-bit counteredge extraction against any proposed compact update rule
a formal theorem that the measure is fixed before horizon extension and decreases under every future lift
```

Cross-problem transfer:

1. RH: a zero grammar repaired by a height-dependent coordinate is not enough; it must become a compact positive-kernel theorem or yield an off-critical pressure counterexample.
2. Goldbach: a margin grammar repaired by cutoff-dependent constants is not enough; constants must be fixed before extension or produce an exceptional-residue counterexample.
3. Twin Prime: an exact-gap selector repaired by range-dependent leakage coordinates is not enough; fixed selector mass must survive extension or produce a leakage cycle.
4. Collatz: the next real proof route is no longer scalar clause-rank; it must be ordinal/stateful and horizon-independent.

Remaining decisive target:

```text
CO-TICKET-47 OrdinalStatefulMeasureOr29BitCounteredge
```

Proof boundary:

```text
TICKET-46 does not prove or disprove any of the four open problems. It proves a restricted no-go result for the tested finite scalar template-local clause-rank proof routes, and it moves the Collatz proof attempt to a sharper target: a horizon-independent ordinal/stateful measure or a future counteredge against such a measure.
```

### Ticket 47: Periodic state lasso lab

Generated artifact:

```text
data/open-problem/ticket47-periodic-state-lasso-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-47-zero-lasso-automaton.json
data/open-problem/collatz/co-ticket-47-periodic-state-lasso.json
data/open-problem/goldbach/gb-ticket-47-margin-lasso-automaton.json
data/open-problem/twin-prime/tp-ticket-47-gap-lasso-automaton.json
```

Aggregate verdict:

```text
periodic_state_lasso_restricted_no_go_open_no_resolution
```

한국어 요약: TICKET-47은 TICKET-46의 scalar clause-rank 폐기 결과를 한 단계 더 밀어붙인다. 단순 scalar rank가 안 되면 bounded memory를 붙인 stateful automaton으로 살릴 수 있는지 묻는다. 28-bit exact-template pressure graph에서 16-edge positive-debt lasso를 추출했고, zero-memory 및 last-1부터 last-4 edge-signature memory까지 모두 한 period 뒤 같은 expanded state로 되돌아오는 것을 확인했다. 따라서 이 bounded suffix-memory 수리 계열은 strict well-founded descent가 될 수 없다. 하지만 이것도 Collatz 반례는 아니다. 이 cycle은 abstract template pressure relation의 lasso이며, 하나의 실제 Collatz orbit으로 reachable하다는 증명은 아직 없다.

English summary: TICKET-47 upgrades the TICKET-46 scalar-rank obstruction to a bounded-memory stateful obstruction. It extracts a 16-edge positive-debt lasso from the 28-bit exact-template pressure graph. Zero-memory and last-1 through last-4 edge-signature memory automata all return to the same expanded state after one lasso period, so none of these bounded suffix-memory repairs can support a strict well-founded descent. This is still not a Collatz counterexample: the lasso is an abstract template-pressure object, not a certified single reachable orbit.

Collatz periodic-lasso audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
28-bit pressure edges: 741,372
raw open edges processed: 7,960,722
lasso cycle edges: 16
unique edge symbols: 16
total max delta debt over period: 5.84962500721
tested bounded-memory automata: 5
refuted bounded-memory automata: 5
```

Tested stateful repairs:

```text
zero_memory_pressure_lasso: refuted_by_periodic_pressure_lasso
last1_edge_signature: refuted_by_periodic_pressure_lasso
last2_edge_signature: refuted_by_periodic_pressure_lasso
last3_edge_signature: refuted_by_periodic_pressure_lasso
last4_edge_signature: refuted_by_periodic_pressure_lasso
```

First lasso edge:

```text
[0,[1,1,1,1],103,1] -> [1,[1,1,1,1],103,1]
symbol: dir=low|label=both_open|dp=1|dc=1|phase=0->1|v=1->1
max delta debt: 0.584962500721
```

Discarded Collatz routes:

```text
zero-memory exact-template pressure rank
bounded suffix-memory stateful repair using last 1-4 pressure-edge signatures
any proof object that silently treats a periodic bounded-memory lasso as a strict descent
```

Retained Collatz routes:

```text
prove that the abstract pressure lasso is unreachable by any concrete Collatz lift path
synthesize arbitrary small finite-state automata and refute them by CEGIS rather than only suffix memory
define a genuinely ordinal/stateful measure whose state is fixed before horizon extension and is not bounded suffix memory
push surviving automata to 29-bit/30-bit reachability stress
```

Cross-problem transfer:

1. RH: a bounded zero-state memory that repeats on an off-critical kernel lasso cannot prove zero exclusion.
2. Goldbach: a bounded cutoff ledger that repeats on an exceptional-residue margin lasso cannot prove positivity.
3. Twin Prime: a bounded leakage memory that repeats on a wider-gap lasso cannot prove exact gap-2 infinitude.
4. Collatz: stateful repairs must now pass lasso reachability or arbitrary finite-automaton CEGIS, not just bounded suffix memory.

Remaining decisive target:

```text
CO-TICKET-48 AutomatonCEGISOr29BitReachability
```

Proof boundary:

```text
TICKET-47 does not prove or disprove any of the four open problems. It proves a restricted no-go result for bounded suffix-memory repairs over the 28-bit abstract template pressure lasso. It does not prove the lasso is a single reachable Collatz orbit and does not refute arbitrary finite automata or ordinal-valued measures.
```

### Ticket 48: Automaton reachability lab

Generated artifact:

```text
data/open-problem/ticket48-automaton-reachability-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-48-kernel-period-map.json
data/open-problem/collatz/co-ticket-48-automaton-reachability.json
data/open-problem/goldbach/gb-ticket-48-margin-period-map.json
data/open-problem/twin-prime/tp-ticket-48-gap-period-map.json
```

Aggregate verdict:

```text
automaton_reachability_split_open_no_resolution
```

한국어 요약: TICKET-48은 TICKET-47의 약한 고리를 둘로 나눴다. 첫째, 추상 template-pressure lasso가 반복 가능하다고 가정하면 bounded suffix-memory뿐 아니라 임의의 고정된 유한상태 total deterministic update도 strict descent를 만들 수 없다. 한 period가 finite state set 위의 함수 \(F:S\to S\)를 만들고, \(F\)를 반복하면 어떤 state가 다시 나타나므로 template/state expanded quotient에서 finite directed cycle이 생기기 때문이다. 둘째, 이 추상 lasso가 실제 Collatz residue lift path로 이어지는지를 별도 bounded probe로 검사했다. 28-bit frontier 안에서는 start-template candidate 4개를 찾았고, 그중 concrete positive step은 2단계까지 이어졌지만 3단계에서 surviving transition이 0개가 되어 한 period도 완성하지 못했다.

English summary: TICKET-48 separates the abstract automaton obstruction from concrete Collatz reachability. Conditional on the repeatable abstract lasso, any fixed finite total deterministic state update induces a one-period map on a finite state set, and iterating that map eventually repeats the expanded template/state while the abstract lasso carries positive pressure debt. A bounded concrete lift probe then checks whether the same lasso can be realized by compatible residues. It finds four start-template candidates and two positive concrete steps, but no surviving transition at the third step and no complete positive-pressure period.

Collatz automaton/reachability audit:

```text
28-bit template nodes: 261,367
28-bit template edges: 1,370,168
28-bit pressure edges: 741,372
raw open edges processed: 7,960,722
lasso cycle edges: 16
total max delta debt over abstract period: 5.84962500721
finite-state period-map rows: 9
start-template candidates in bounded frontier: 4
concrete lasso steps completed: 3 checked, 0 survivors at step 3
best concrete partial depth: 2
best concrete partial debt: 1.169925001442
```

Discarded Collatz routes:

```text
any fixed finite total deterministic state repair over the repeatable abstract lasso
any finite quotient proof that silently treats the abstract lasso as a strict descent object
any claim that TICKET47/TICKET48 already supplies a Collatz counterexample without concrete infinite reachability
```

Retained Collatz routes:

```text
prove the TICKET47/TICKET48 lasso family is unreachable by all concrete residue lifts
find a concrete periodic lift witness at a larger horizon and test whether it repeats unboundedly
define a genuinely ordinal or unbounded-state measure fixed before horizon extension
turn the reachability probe into a symbolic preimage automaton rather than relying on sampled starts
```

Cross-problem transfer:

1. RH: a finite kernel-state repair cannot certify zero exclusion if a repeatable off-critical zero lasso remains reachable.
2. Goldbach: a finite cutoff-state repair cannot certify positivity if an exceptional-residue margin lasso remains reachable.
3. Twin Prime: a finite selector-state repair cannot certify exact gap-2 infinitude if wider-gap leakage lassos remain reachable.
4. Collatz: the next target is not another finite automaton wrapper; it is reachability exclusion, concrete periodic lift extraction, or a non-finite-state descent theorem.

Remaining decisive target:

```text
CO-TICKET-49 SymbolicReachabilityExclusionOrConcretePeriodicLift
```

Proof boundary:

```text
TICKET-48 does not prove or disprove any of the four open problems. It proves a conditional abstract no-go for fixed finite total deterministic state repairs over the extracted Collatz template lasso and reports a bounded concrete reachability failure through one full period. The unresolved theorem is still infinite: either exclude the lasso family for all future residue lifts, or produce a certified unbounded concrete lift witness.
```

### Ticket 49: Symbolic preimage obstruction lab

Generated artifact:

```text
data/open-problem/ticket49-symbolic-preimage-obstruction-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-49-zero-kernel-preimage.json
data/open-problem/collatz/co-ticket-49-symbolic-preimage-obstruction.json
data/open-problem/goldbach/gb-ticket-49-residue-margin-preimage.json
data/open-problem/twin-prime/tp-ticket-49-gap-selector-preimage.json
```

Aggregate verdict:

```text
symbolic_preimage_obstruction_open_no_resolution
```

한국어 요약: TICKET-49는 TICKET-48의 concrete reachability 실패를 “왜 실패했는가”까지 좁힌다. 16-bit phase-compatible start template `[0,[1,1,1,1],103,1]`을 만족하는 residue는 정확히 4개다. forced-low lasso prefix에서 이들은 step 1 뒤 2개, step 2 뒤 1개, step 3 뒤 0개가 된다. 마지막 생존 residue는 세 번째 phase에서 phase, tail word, residue mod 256은 맞지만 `next_valuation = 5`가 되어, lasso가 요구하는 `next_valuation = 1`과 충돌한다.

English summary: TICKET-49 turns the TICKET-48 reachability failure into a coordinate-level obstruction. The exact 16-bit phase-compatible start set has four residues. Along the forced-low lasso prefix, the survivor counts are 4 -> 2 -> 1 -> 0. The unique two-step survivor reaches the third phase with the correct phase, tail word, and residue mod 256, but with next valuation 5 rather than the lasso-required 1.

Collatz symbolic-preimage audit:

```text
start template: [0,[1,1,1,1],103,1]
start candidates: 26471, 28007, 34919, 48743
forced-low survivors: 4 -> 2 -> 1 -> 0
dead step: 3
obstruction coordinate: next_valuation
required third template: [3,[1,1,1,1],103,1]
observed third template on the unique survivor: [3,[1,1,1,1],103,5]
best partial depth: 2
best partial debt: 1.169925001442
```

Discarded Collatz routes:

```text
blindly rerunning larger frontier probes without naming the failed coordinate
claiming the abstract TICKET47/TICKET48 lasso is concrete after only two matching steps
treating finite-state or bounded-prefix failure as a Collatz proof
```

Retained Collatz routes:

```text
prove the next_valuation obstruction for every b == 0 mod 16 compatible lift
derive a symbolic preimage recurrence for the third low-prefix step
search for a higher-bit exception that changes next_valuation 5 back to 1
if such an exception exists, test whether it can complete and repeat the full lasso period
```

Cross-problem transfer:

1. RH: after a zero-kernel lasso attempt fails, identify the first failed kernel coordinate before proposing a larger automaton.
2. Goldbach: after a residue-margin lasso attempt fails, identify whether the obstruction is residue class, singular-series margin, or cutoff leakage.
3. Twin Prime: after a gap-selector lasso attempt fails, identify whether exact gap-2 mass fails at selector state or leakage class.
4. Collatz: the next theorem is now a next-valuation preimage theorem, not another finite-state wrapper.

Remaining decisive target:

```text
CO-TICKET-50 AllPhaseNextValuationPreimageOrHigherBitException
```

Proof boundary:

```text
TICKET-49 does not prove or disprove any of the four open problems. It identifies the first local coordinate that blocks the 16-bit Collatz lasso-prefix realization. The unresolved theorem is still infinite: prove the same next-valuation obstruction for every compatible modulus, or find a higher-bit exception and test whether it becomes an unbounded concrete lasso.
```

### Ticket 50: Phase-lift exception lab

Generated artifact:

```text
data/open-problem/ticket50-phase-lift-exception-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-50-zero-kernel-exception.json
data/open-problem/collatz/co-ticket-50-phase-lift-exception.json
data/open-problem/goldbach/gb-ticket-50-residue-margin-exception.json
data/open-problem/twin-prime/tp-ticket-50-gap-selector-exception.json
```

Aggregate verdict:

```text
phase_lift_exception_open_no_resolution
```

한국어 요약: TICKET-50은 TICKET-49의 16비트 장애물을 무시하지 않는다. 오히려 그 장애물을 전역 정리로 승격할 수 있는지 시험했고, 32비트 phase-compatible lift에서 반례를 찾았다. 즉 “모든 b == 0 mod 16에서 세 번째 low-prefix의 `next_valuation = 1`은 불가능하다”는 프로젝트 내부 후보 정리는 틀렸다. 대신 32비트에서 훨씬 강한 near-lasso 후보 2개가 발견됐다. 이들은 16개 lasso-prefix 템플릿 중 15개까지 따라가지만 마지막 phase에서 tail shift 또는 all_lift_descent로 실패한다.

English summary: TICKET-50 does not discard TICKET-49. It stress-tests the proposed all-phase extension and refutes that project-local candidate theorem at 32 bits. The same start template has 69,092 exact valuation-word matches, 8,684 four-consecutive-one low-lift exceptions, and two near-lasso witnesses that match 15 of the 16 lasso-prefix templates before terminal failure.

Exact Collatz audit:

```text
valuation-run lemma: r consecutive accelerated valuations equal 1 iff boundary x == -1 mod 2^(r+1)
16-bit start-template matches: 4
16-bit four-consecutive-one exceptions: 0
16-bit max lasso-prefix depth: 3
32-bit start-template matches: 69,092
32-bit four-consecutive-one exceptions: 8,684
32-bit max lasso-prefix depth: 15
32-bit depth counts: {1: 34,458; 2: 17,301; 3: 8,649; 4: 4,310; 5: 4,372; 15: 2}
```

Discarded Collatz route:

```text
the TICKET-49 all-phase next_valuation obstruction as stated
any proof route that treats the 16-bit obstruction as universal without checking higher phase-compatible lifts
```

Retained and strengthened Collatz routes:

```text
classify every 48-bit child of the two 32-bit depth-15 near-lasso residues
prove the phase-15 terminal obstruction for all descendants, or find a child that completes the final lasso template
if a full lasso completion appears, replay it as a concrete periodic-lift candidate before making any counterexample claim
```

Cross-problem transfer:

1. RH: if a local zero-kernel obstruction fails at a higher height, promote the zero-kernel exception and classify the terminal coordinate.
2. Goldbach: if a residue-margin obstruction fails at a larger cutoff, promote the exceptional even integer or character instead of discarding it.
3. Twin Prime: if an exact-gap selector obstruction fails at a larger sieve level, promote the surviving gap-2 packet as the next stress witness.
4. Collatz: the active target is now a phase-15 terminal lift theorem or a 48-bit completion witness.

Remaining decisive target:

```text
CO-TICKET-51 Phase15TerminalLiftOrFullLassoCompletion
```

Proof boundary:

```text
TICKET-50 does not prove or disprove any of the four open problems. It refutes one PrimeProject candidate obstruction and creates stronger finite stress witnesses. The unresolved theorem remains infinite: either all descendants of the near-lasso witnesses terminate by descent/tail shift, or a concrete lift completes and repeats the lasso.
```

### Ticket 51: Phase-15 terminal lift closure

Generated artifact:

```text
data/open-problem/ticket51-phase15-terminal-lift-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-51-terminal-witness-closure.json
data/open-problem/collatz/co-ticket-51-phase15-terminal-lift.json
data/open-problem/goldbach/gb-ticket-51-terminal-witness-closure.json
data/open-problem/twin-prime/tp-ticket-51-terminal-witness-closure.json
```

Aggregate verdict:

```text
phase15_terminal_lift_closed_open_no_resolution
```

한국어 요약: TICKET-51은 TICKET-50에서 발견된 두 개의 32-bit depth-15 near-lasso residue를 반례 후보로 방치하지 않는다. 각 residue에서 phase-15로 가는 low/high lift를 모두 열어 terminal branch를 분류했다. 결과적으로 surviving branch는 0개다. 두 branch는 `tail_word+next_valuation` shift로 lasso template을 벗어나고, 두 branch는 `all_lift_descent`로 닫힌다.

English summary: TICKET-51 terminally classifies the two strongest 32-bit near-lasso witnesses from TICKET-50. Opening every low/high branch through the missing phase-15 edge leaves zero survivors: two branches shift the tail and next valuation, and two branches close by all-lift descent.

Exact Collatz audit:

```text
source roots: 1471663463, 3206130791
base bits: 32
terminal step: 15
tested terminal branches: 4
matching terminal branches: 0
final surviving states: 0
full lasso completions: 0
best template depth: 15
terminal mismatch counts: {all_lift_descent: 2, tail_word+next_valuation: 2}
```

Discarded Collatz route:

```text
using either TICKET-50 depth-15 residue as a concrete Collatz counterexample candidate
relifting the same two roots without a new terminal theorem
```

Retained Collatz routes:

```text
search for genuinely new 48-bit or 64-bit start-template roots with lasso-prefix depth >= 15
derive a symbolic theorem explaining why phase-15 terminal branches always shift or descend
if a future root completes the full lasso, replay it for at least two periods before any counterexample claim
```

Remaining decisive target:

```text
CO-TICKET-52 New48Or64BitRootSearchOrTerminalTheorem
```

Proof boundary:

```text
TICKET-51 does not prove or disprove any of the four open problems. It closes only the terminal lift tree descending from the two known 32-bit near-lasso roots. It does not exclude new 48-bit roots outside that ancestry and does not prove global Collatz descent.
```

### Ticket 52: 48-bit frontier budget and sampled witness closure

Generated artifact:

```text
data/open-problem/ticket52-frontier-budget-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-52-frontier-budget-contract.json
data/open-problem/collatz/co-ticket-52-frontier-budget-sample-closure.json
data/open-problem/goldbach/gb-ticket-52-frontier-budget-contract.json
data/open-problem/twin-prime/tp-ticket-52-frontier-budget-contract.json
```

Aggregate verdict:

```text
frontier_budget_open_no_resolution
```

한국어 요약: TICKET-52는 TICKET-51의 한계를 정면으로 확인한다. TICKET-51은 두 개의 32비트 near-lasso ancestry를 닫았지만, 48비트 start-template root가 반드시 그 두 ancestry로 투영되는 것은 아니다. 실제로 재현 가능한 200,000개 debt-valid valuation-word 샘플에서 새 48비트 depth-15 near-lasso root `171308122831719`가 발견됐고, 이 root의 32비트 projection은 `[0,[1,2,1,1],103,2]`라서 기존 닫힌 start-template ancestry 밖에 있다. 이 새 후보도 base-48 terminal lift audit에서 phase 15에 닫혔다.

English summary: TICKET-52 shows that the TICKET-51 closure is ancestry-local, not a 48-bit theorem. The exact 48-bit frontier has 83,401,400,116 debt-valid valuation words, and a deterministic 200,000-word sampler finds one new 48-bit depth-15 near-lasso root outside the closed 32-bit ancestry. A generalized base-48 terminal lift audit closes that witness at phase 15 with no full lasso completion.

Exact Collatz audit:

```text
48-bit debt-valid valuation words: 83,401,400,116
64-bit debt-valid valuation words: 2,216,134,944,775,156
sample seed: 20,260,709
sample count: 200,000
verified open sample words: 100,026
start-template sample matches: 3,184
sampled depth counts: {1: 1,650; 2: 763; 3: 406; 4: 189; 5: 175; 15: 1}
new sampled depth-15 root: 171308122831719
32-bit projection: 3352230759
projection template: [0,[1,2,1,1],103,2]
terminal step: 15
terminal mismatch counts: {tail_word+next_valuation: 2}
final surviving states: 0
full lasso completions: 0
```

Discarded Collatz route:

```text
promoting the TICKET51 two-root closure to a 48-bit theorem
continuing with blind 48-bit or 64-bit valuation-word enumeration as the main proof route
treating a sampled closure as evidence that all unsampled roots close
```

Retained Collatz routes:

```text
build a symbolic counter for all 48-bit start-template roots
encode the valuation-word frontier as a SAT/SMT or automaton-counting problem
prove a phase-15 terminal mismatch theorem for every depth-15 root
if a future root completes the full lasso, replay it for multiple periods and then state the independent infinite periodicity theorem required
```

Remaining decisive target:

```text
CO-TICKET-53 Symbolic48BitFrontierCoverageOrFullLassoReplay
```

Proof boundary:

```text
TICKET-52 does not prove or disprove any of the four open problems. It finds and closes one new sampled 48-bit Collatz near-lasso witness, and it proves that the old valuation-word enumeration has reached an infeasible frontier. The sampler is not exhaustive and cannot exclude unsampled 48-bit roots.
```

### Ticket 53: Symbolic phase-15 terminal mismatch theorem

Generated artifact:

```text
data/open-problem/ticket53-symbolic-terminal-theorem-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-53-terminal-no-go-theorem.json
data/open-problem/collatz/co-ticket-53-symbolic-terminal-theorem.json
data/open-problem/goldbach/gb-ticket-53-terminal-no-go-theorem.json
data/open-problem/twin-prime/tp-ticket-53-terminal-no-go-theorem.json
```

Aggregate verdict:

```text
symbolic_terminal_theorem_open_no_resolution
```

한국어 요약: TICKET-53은 TICKET-50부터 TICKET-52까지 반복된 phase-15 terminal failure를 더 큰 샘플로 밀어붙이지 않고, 상징 정리로 분리한다. 현재 추출된 lasso family에서 phase 14 parent가 `[14,[1,1,1,1],103,10]`이면, low terminal branch는 대기 중인 valuation `10`을 정확히 소비하므로 tail에 `10`이 들어간다. high terminal branch는 prefix 이후 boundary가 `3^m * 2^9`만큼 바뀌므로 next valuation이 `9`로 강제된다. 따라서 두 branch 모두 phase-15 target `[15,[1,1,1,1],103,10]`에 도달할 수 없다.

English summary: TICKET-53 converts the repeated terminal failure into a local theorem. For the extracted lasso family, a phase-14 parent with template `[14,[1,1,1,1],103,10]` cannot reach the phase-15 target on either branch. The low branch consumes the pending valuation `10`, forcing a tail mismatch. The high branch shifts the boundary by `3^m * 2^9`, forcing next valuation `9`, so it also cannot match the target.

Exact Collatz audit:

```text
theorem: Phase15TerminalMismatchForExtractedLasso
checked roots: 1471663463 at 32 bits; 3206130791 at 32 bits; 171308122831719 at 48 bits
all checked roots satisfy parent premise: true
low branch next valuation before terminal: 10
high branch next valuation before terminal: 9
terminal target matches: 0
```

Discarded Collatz route:

```text
the extracted phase-15 lasso family as a counterexample route
larger sampling inside the same terminal template family
relifting known roots after the symbolic mismatch theorem already applies
```

Retained Collatz routes:

```text
extract genuinely new lasso-template families from the frontier graph
search for a global descent invariant not based on the discarded phase-15 family
formalize Phase15TerminalMismatchForExtractedLasso in the proof kernel as a local no-go lemma
```

Remaining decisive target:

```text
CO-TICKET-54 NewTemplateFamilyExtractionOrGlobalDescentInvariant
```

Proof boundary:

```text
TICKET-53 does not prove or disprove any of the four open problems. It refutes one extracted Collatz lasso family, including all currently known near-lasso witnesses for that family. A full Collatz proof still requires a global argument covering all trajectories or all remaining template families.
```

### Ticket 54: Post-terminal new template family extraction

Generated artifact:

```text
data/open-problem/ticket54-new-template-family-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-54-post-nogo-family-triage.json
data/open-problem/collatz/co-ticket-54-new-template-family.json
data/open-problem/goldbach/gb-ticket-54-post-nogo-family-triage.json
data/open-problem/twin-prime/tp-ticket-54-post-nogo-family-triage.json
```

Aggregate verdict:

```text
new_template_family_extracted_open_no_resolution
```

한국어 요약: TICKET-54는 TICKET-53에서 폐기된 phase-15 terminal family를 더 이상 샘플링하지 않는다. 대신 그 family를 제거한 뒤 남는 Collatz frontier를 다시 세어, 다음으로 공격해야 할 family를 추출한다. exact 32-bit 시작 template은 69,092개이고, 이 중 TICKET-53이 폐기한 depth-15 root 2개를 제거하면 69,090개가 남는다. 남은 후보의 최대 lasso-prefix depth는 5로 내려가며, 4,372개가 phase-5 `next_valuation=10` gate에서 막힌다. 이 phase-5 실패군 안에서 observed next valuation이 10인 경우는 0개다.

English summary: TICKET-54 stops spending search budget on the TICKET-53 terminal family. It removes that family, re-audits the remaining exact 32-bit start-template frontier, and extracts `Phase5ValuationGate` as the strongest remaining bounded Collatz family. The post-discard frontier has max depth 5, with 4,372 exact roots failing at the phase-5 next-valuation gate.

Exact Collatz audit:

```text
exact 32-bit start-template matches: 69,092
discarded TICKET-53 depth-15 roots: 2
remaining exact starts: 69,090
post-discard max exact depth: 5
phase-5 gate exact roots: 4,372
phase-5 failures with observed next_valuation=10: 0
48-bit deterministic sample post-discard max depth: 5
48-bit deterministic sample phase-5 gate roots: 175
```

New candidate family:

```text
Phase5ValuationGate
```

Candidate theorem:

```text
Every phase-compatible start that reaches the first five lasso templates either belongs to the discarded phase-15 terminal family, closes by descent, or fails the phase-5 next_valuation=10 gate.
```

Counterexample target:

```text
Find a root outside the TICKET-53 terminal family that reaches phase 5 with next_valuation=10 and then survives into a different replayable lasso template.
```

Discarded or deprioritized routes:

```text
repeating random samples inside the TICKET-53 terminal family
treating the 26-bit finite template-rank measure as a Collatz proof
blindly enlarging the template graph without a parametric closure theorem
```

Remaining decisive target:

```text
CO-TICKET-55 Phase5ValuationGateTheoremOrCounterexample
```

Proof boundary:

```text
TICKET-54 does not prove or disprove any of the four open problems. It prunes one terminal family and extracts the next finite Collatz family to attack. A full Collatz proof still requires an all-lift phase-5 gate theorem, a global descent invariant, or a genuine replayable counterexample.
```

### Ticket 55: Phase-5 gate-to-terminal tunnel theorem

Generated artifact:

```text
data/open-problem/ticket55-phase5-valuation-gate-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-55-gate-terminal-tunnel.json
data/open-problem/collatz/co-ticket-55-phase5-gate-tunnel.json
data/open-problem/goldbach/gb-ticket-55-gate-terminal-tunnel.json
data/open-problem/twin-prime/tp-ticket-55-gate-terminal-tunnel.json
```

Aggregate verdict:

```text
phase5_gate_tunnel_open_no_resolution
```

한국어 요약: TICKET-55는 TICKET-54에서 남은 `Phase5ValuationGate`를 더 큰 샘플로 키우지 않고, gate를 통과한 후보가 어디로 가는지 증명 의무를 분리한다. phase 5에서 `[5,[1,1,1,1],103,10]`에 도달하고 `consumed_bits = b+5`이면, pending valuation `10`은 phase 6부터 phase 14까지 소비되지 않는다. 따라서 같은 prefix, 같은 consumed bit count, 같은 next valuation을 유지한 채 phase 좌표만 증가한다. phase 15에서는 그 `10`이 소비되어 tail이 `[1,1,1,10]`으로 바뀌거나 descent로 닫히므로, target `[15,[1,1,1,1],103,10]`에는 도달하지 못한다.

English summary: TICKET-55 proves a local gate-to-terminal tunnel for the extracted low-lift family. If a root reaches the phase-5 gate with consumed bits equal to the gate modulus, the pending valuation `10` survives unchanged through phases 6-14. At phase 15 it is consumed, forcing the TICKET53 terminal no-go.

Exact Collatz audit:

```text
theorem: Phase5GateToTerminalTunnel
checked gate-crossing roots: 3
gate matches: 3
tunnel matches through phases 5-14: 3
same pending certificate through tunnel: 3
terminal target matches: 0
exact 32-bit start-template matches: 69,092
exact 32-bit starts failed before or at phase 5: 69,090
exact 32-bit gate crossers: 2
exact 32-bit gate crossers terminally closed: 2
48-bit deterministic sample phase-5 gate roots: 175
```

Local theorem:

```text
Phase5GateToTerminalTunnel
```

Candidate theorem still missing:

```text
Every phase-compatible start outside the current low-lift family either fails before or at a finite valuation gate, or enters a separately terminally closed family.
```

Counterexample target:

```text
Find a root outside the current low-lift start-template model that crosses the finite gate and avoids every known terminal no-go tunnel.
```

Remaining decisive target:

```text
CO-TICKET-56 PreGateResidueClosureOrTemplateModelEscape
```

Proof boundary:

```text
TICKET-55 does not prove or disprove any of the four open problems. It closes the extracted low-lift lasso route for the exact 32-bit start-template population and the known 48-bit sampled gate-crosser, but it does not cover every Collatz trajectory, every base modulus, or every possible template family.
```

### Ticket 56: Pre-gate partition and projection escape

Generated artifact:

```text
data/open-problem/ticket56-pre-gate-projection-escape-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-56-projection-escape-frontier.json
data/open-problem/collatz/co-ticket-56-pre-gate-projection-escape.json
data/open-problem/goldbach/gb-ticket-56-lift-escape-frontier.json
data/open-problem/twin-prime/tp-ticket-56-lift-escape-frontier.json
```

Aggregate verdict:

```text
pre_gate_projection_escape_open_no_resolution
```

한국어 요약: TICKET-56은 TICKET-55 이후 남은 가장 쉬운 오해를 제거한다. exact 32-bit start-template 안에서는 현재 추출된 lasso route가 완전히 분할된다. `69,092`개 후보 중 `69,090`개는 offset 1-5에서 next-valuation mismatch로 실패하고, 남은 `2`개 gate crosser는 TICKET-55에서 terminal no-go로 닫혔다. 하지만 이 finite partition을 전역 귀납으로 올리는 것은 틀린 경로다. TICKET-52에서 기록된 48-bit depth-15 witness `171308122831719`는 32-bit projection이 `[0,[1,2,1,1],103,2]`라서 exact32 start-template 밖으로 벗어난다.

English summary: TICKET-56 closes the exact 32-bit extracted-lasso route as a finite partition, then rejects the simple projection-closure route. A higher-bit start-template witness can project outside the fixed 32-bit start-template model, so the next theorem must be parametric in base modulus and template state.

Exact Collatz audit:

```text
local theorem: Exact32StartTemplateLassoPartition
exact 32-bit start-template matches: 69,092
pre-gate first failures: 69,090
failure offsets: 1 -> 34,458; 2 -> 17,301; 3 -> 8,649; 4 -> 4,310; 5 -> 4,372
all pre-gate failures are next-valuation mismatch: true
phase-5 observed next_valuation=10 among failures: 0
gate crossers: 2
partition sum: 69,092
partition complete for exact32 start-template: true
projection-closure status: refuted by sampled 48-bit depth-15 witness
escape witness: 171,308,122,831,719
```

Discarded route:

```text
A proof that partitions only the exact 32-bit start-template population and assumes every higher-bit start-template root projects back into that same 32-bit template.
```

Candidate theorem still missing:

```text
For every phase-compatible base modulus, every extracted-lasso start-template state either fails a finite next-valuation gate, enters a terminal no-go tunnel, or maps into a strictly smaller closed template family under a well-founded parametric rank.
```

Counterexample target:

```text
Find a higher-bit start-template root outside the exact32 projection model that reaches a finite gate, avoids the TICKET53/TICKET55 terminal tunnel, and replays through at least one full lasso period.
```

Remaining decisive target:

```text
CO-TICKET-57 ParametricTemplateAutomatonOrEscapeCycle
```

Proof boundary:

```text
TICKET-56 does not prove or disprove any of the four open problems. It proves only a finite partition for one extracted Collatz lasso route at 32 bits and identifies why simple projection-based globalization fails.
```

### Ticket 57: Parametric boundary-state automaton audit

Generated artifact:

```text
data/open-problem/ticket57-parametric-template-automaton-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-57-boundary-state-model.json
data/open-problem/collatz/co-ticket-57-parametric-template-automaton.json
data/open-problem/goldbach/gb-ticket-57-boundary-margin-model.json
data/open-problem/twin-prime/tp-ticket-57-boundary-sieve-model.json
```

Aggregate verdict:

```text
parametric_boundary_state_open_no_resolution
```

한국어 요약: TICKET-57은 TICKET-56 이후의 가장 중요한 약한 지점을 공격한다. exact32 finite partition이 있더라도, 그 분기 결과가 단순 template state로 결정되지 않으면 전역 automaton 증명으로 올릴 수 없다. 계산 결과 template만으로는 6개의 coarse outcome이 한 상태에 섞이고, `template + prefix_length + residue mod 2^26`까지 추가해도 92개 collision group이 남는다. audited ladder에서 처음으로 exact32 coarse outcome이 결정되는 경계는 `template + prefix_length + residue mod 2^28`이다. 또한 알려진 near-lasso root 3개는 최대 depth 15까지만 재생되고 full lasso period replay는 0개다.

English summary: TICKET-57 rejects the shortcut from a finite template quotient to a proof. The exact32 partition needs boundary coordinates before even its bounded outcomes become deterministic. The first deterministic audited boundary is `template + prefix_length + residue mod 2^28`, and no known near-lasso root replays a full lasso period.

Exact Collatz audit:

```text
local theorem target: AffineBoundaryTemplateStateOrEscapeCycle
exact 32-bit start-template matches: 69,092
coarse outcomes: fail_offset_1 -> 34,458; fail_offset_2 -> 17,301; fail_offset_3 -> 8,649; fail_offset_4 -> 4,310; fail_offset_5 -> 4,372; phase5_gate_terminal_tunnel -> 2
template-only max outcomes per state: 6
template + prefix_length + residue mod 2^26 collision groups: 92
first deterministic exact32 boundary: template + prefix_length + residue mod 2^28
projection escape carried forward: sampled 48-bit depth-15 witness 171,308,122,831,719 projects to [0,[1,2,1,1],103,2]
known near-lasso roots replayed: 3
maximum replayed prefix depth: 15
full lasso period replays: 0
cycle status: no_known_root_replays_full_lasso_period
```

Discarded routes:

```text
template-only rank or transition relation
exact32 finite partition promoted by simple projection closure
near-lasso prefix treated as a counterexample without full-period replay and lift compatibility
```

Candidate theorem still missing:

```text
For every phase-compatible start cylinder, a boundary-state transition either reaches a finite next-valuation failure gate, enters the Phase5GateToTerminalTunnel, or strictly decreases a well-founded rank defined on the full affine boundary state.
```

Counterexample target:

```text
Find a higher-bit root whose full affine boundary state returns after one lasso period with nondecreasing rank and whose trajectory is not covered by TICKET53, TICKET55, or TICKET56.
```

Remaining decisive target:

```text
CO-TICKET-58 AffineBoundaryLiftStabilityOrFullPeriodEscape
```

Proof boundary:

```text
TICKET-57 does not prove or disprove any of the four open problems. It rejects weaker finite-state proof shortcuts and finds no replayable cycle among known near-lasso roots; the remaining obligation is a parametric affine-boundary lift theorem or a new full-period escape witness.
```

### Ticket 58: Affine-boundary lift stability audit

Generated artifact:

```text
data/open-problem/ticket58-affine-boundary-lift-lab.json
```

Per-problem artifacts:

```text
data/open-problem/riemann/rh-ticket-58-zero-kernel-lift-stability.json
data/open-problem/collatz/co-ticket-58-affine-boundary-lift.json
data/open-problem/goldbach/gb-ticket-58-margin-lift-stability.json
data/open-problem/twin-prime/tp-ticket-58-sieve-boundary-lift.json
```

Aggregate verdict:

```text
affine_boundary_lift_open_no_resolution
```

한국어 요약: TICKET-58은 TICKET-57에서 처음 결정적이었던 exact32 affine boundary가 48-bit lift에서도 유지되는지 검사한다. 같은 TICKET52 deterministic 48-bit sample을 재생한 결과, start-template match `3,184`개 중 `3,086`개가 exact32 target 밖으로 projection escape했다. exact32 target 안으로 들어온 `98`개 중 `28`개만 exact32 boundary prediction과 맞았고, `70`개는 다른 outcome을 보였다. 따라서 “exact32 deterministic boundary를 그대로 lift하면 된다”는 경로는 샘플에서 반박된다. full lasso period를 재생한 샘플은 0개다.

English summary: TICKET-58 tests lift stability for the first deterministic exact32 affine boundary. The replayed 48-bit sample refutes the unchanged-boundary lift shortcut: most start-template matches project outside the exact32 target, and most projection-target lifts disagree with the exact32 predicted outcome.

Exact Collatz audit:

```text
local theorem target: AffineBoundaryLiftStabilityOrFullPeriodEscape
exact32 boundary width: 28 low bits
exact32 boundary states: 69,092
exact32 boundary collisions: 0
48-bit replayed sample count: 200,000
verified open words: 100,027
48-bit start-template matches: 3,184
projection escapes: 3,086
projection-target lifts: 98
boundary prediction matches: 28
boundary prediction mismatches: 70
projection-target prediction rate: 28.57%
full lasso period replays: 0
lift-stability status: refuted_by_sampled_boundary_prediction_mismatch
```

Discarded route:

```text
Promote the exact32 deterministic boundary to a global theorem without proving projection inclusion and lift-stable outcome preservation.
```

Candidate theorem still missing:

```text
For every 48-bit and then every higher phase-compatible start, either projection leaves the exact32 model in a separately classified way, or the affine boundary transition preserves the finite gate outcome and decreases a well-founded rank.
```

Counterexample target:

```text
Find a higher-bit start whose projection lies in the deterministic exact32 boundary but whose lift outcome differs, then extend it to a full-period nondecreasing affine-boundary cycle.
```

Remaining decisive target:

```text
CO-TICKET-59 SymbolicLiftMismatchCylinderOrCounted40BitCover
```

Proof boundary:

```text
TICKET-58 does not prove or disprove any of the four open problems. It refutes one sampled lift-stability shortcut and finds no sampled full-period escape; the remaining obligation is symbolic coverage of projection escapes/lift mismatches or a genuine full-period counterexample.
```

### Ticket 59: Symbolic lift mismatch cylinder audit

CO-TICKET-59 SymbolicLiftMismatchCylinderOrCounted40BitCover

Artifacts:

```text
data/open-problem/ticket59-symbolic-lift-mismatch-lab.json
data/open-problem/collatz/co-ticket-59-symbolic-lift-mismatch.json
data/open-problem/riemann/rh-ticket-59-counted-lift-cylinder.json
data/open-problem/goldbach/gb-ticket-59-counted-margin-cylinder.json
data/open-problem/twin-prime/tp-ticket-59-counted-sieve-cylinder.json
```

Status:

```text
symbolic_lift_mismatch_open_no_resolution
```

한국어 요약: TICKET-59는 TICKET-58의 lift mismatch를 단일 샘플로 두지 않고 low40 cylinder 단위로 묶는다. 각 selected low40 cylinder마다 가능한 256개 48-bit extension을 전부 열거한다. 선택된 162개 cylinder에서 41,472개 extension을 검사했고, 그중 535개가 48-bit start-template lift였다. 이 안에서 projection escape는 207개, projection-target lift는 328개, boundary mismatch는 224개, boundary match는 104개였다. mismatch seed cylinder 70개 중 35개는 uniform mismatch였지만, 58개 selected cylinder는 mixed outcome이었다. 따라서 “TICKET58 mismatch는 단일 우연 샘플일 뿐”이라는 약한 반론은 줄어들지만, low40만으로는 symbolic proof coordinate가 충분하지 않다는 장애물도 동시에 생긴다.

English summary: TICKET-59 promotes the TICKET-58 point mismatch into selected counted low40-to-48 cylinder audits. It exactly enumerates 256 possible 48-bit extensions for each selected low40 cylinder. This strengthens the evidence from point samples to finite cylinder facts, but it also shows that low40 is not yet a complete symbolic coordinate because many selected cylinders have mixed outcomes.

Key Collatz result:

```text
selected low40 cylinders: 162
tested 48-bit extensions: 41,472
48-bit start-template lifts: 535
projection escapes inside selected cylinders: 207
projection-target lifts inside selected cylinders: 328
boundary prediction mismatches: 224
boundary prediction matches: 104
mismatch-seed cylinders: 70
uniform mismatch cylinders: 35
mixed/unstable cylinders: 58
full lasso period escapes: 0
```

Discarded route:

```text
Treat one 48-bit mismatch as an isolated anecdote, or assume low40 cylinders are stable without enumerating their 48-bit extensions.
```

Candidate theorem still missing:

```text
Every projection-target lift cylinder is either uniformly closed by the exact32 boundary prediction, uniformly refutes that prediction, or carries an explicit higher coordinate that separates the outcomes.
```

Counterexample target:

```text
A counted or symbolic cylinder with full-period replay, or a mixed cylinder that forces an additional coordinate not present in the current affine boundary.
```

Remaining decisive target:

```text
CO-TICKET-60 MixedCylinderSeparatorOrAutomatonCountedCover
```

Proof boundary:

```text
TICKET-59 does not prove or disprove any of the four open problems. It is an exact enumeration of selected low40-to-48 cylinders induced by TICKET58, not an exhaustive 40-bit or 48-bit theorem.
```

### Ticket 60: Mixed-cylinder separator audit

CO-TICKET-60 MixedCylinderSeparatorOrAutomatonCountedCover

Artifacts:

```text
data/open-problem/ticket60-mixed-cylinder-separator-lab.json
data/open-problem/collatz/co-ticket-60-mixed-cylinder-separator.json
data/open-problem/riemann/rh-ticket-60-mixed-cylinder-separator.json
data/open-problem/goldbach/gb-ticket-60-mixed-margin-separator.json
data/open-problem/twin-prime/tp-ticket-60-mixed-sieve-separator.json
```

Status:

```text
mixed_cylinder_separator_open_no_resolution
```

한국어 요약: TICKET-60은 TICKET-59에서 남은 58개 mixed low40 cylinder를 대상으로 separator ladder를 만든다. 선택된 전체 집합은 low40 cylinder 162개와 start-template lift 535개이고, mixed cylinder 내부에는 lift 210개가 있다. `low40`만 쓰면 mixed cylinder 58개가 모두 모호하고, `certificate_prefix_length`를 더해도 mixed outcome collision group이 36개 남는다. 처음으로 outcome과 boundary prediction label을 동시에 결정적으로 가르는 좌표는 `low40 + failure_offset`이다. 그러나 `failure_offset`은 trajectory replay를 통해 얻는 진단 좌표이므로, 이것만으로는 증명이 아니다. 다음 목표는 이 offset을 사전에 예측하는 symbolic transition theorem 또는 automaton-counted cover다.

English summary: TICKET-60 identifies the first tested separator for the mixed TICKET59 cylinders. `low40 + failure_offset` deterministically separates both observed outcome and boundary-match status on the selected population. This is a useful coordinate discovery, but it is replay-derived; a proof needs a non-circular symbolic predictor for failure offset.

Key Collatz result:

```text
selected low40 cylinders: 162
selected start-template lifts: 535
mixed cylinders: 58
mixed start-template lifts: 210
low40-only mixed outcome collisions: 58 groups / 210 ambiguous rows
low40 + certificate_prefix_length: 36 outcome collision groups / 81 ambiguous rows
first joint deterministic separator: low40_plus_failure_offset
first high-extension low-bit separator: high_extension mod 2^4
first high-extension top-bit separator: top 6 bits
full proof status: open
```

Discarded route:

```text
Assume low40 cylinder identity is enough to classify higher-bit outcomes. TICKET60 rejects this because 58 selected cylinders remain mixed under low40 alone.
```

Candidate theorem still missing:

```text
Every mixed low40 cylinder is separated by a bounded higher-coordinate signature, and that signature extends to an automaton-counted cover with no full-period nondecreasing cycle.
```

Counterexample target:

```text
A mixed cylinder whose ambiguity survives every bounded separator short of exact high-extension identity, or a full-period replay inside a separated cylinder.
```

Remaining decisive target:

```text
CO-TICKET-61 SymbolicFailureOffsetPredictorOrCountedCover
```

Proof boundary:

```text
TICKET-60 does not prove or disprove any of the four open problems. It names a replay-derived separator and refutes under-specified boundary proofs; the infinite symbolic transition theorem remains open.
```

### Ticket 61: Symbolic failure-offset pre-replay separator audit

CO-TICKET-61 SymbolicFailureOffsetPredictorOrCountedCover

Artifacts:

```text
data/open-problem/ticket61-symbolic-failure-offset-lab.json
data/open-problem/collatz/co-ticket-61-symbolic-failure-offset.json
data/open-problem/riemann/rh-ticket-61-symbolic-separator.json
data/open-problem/goldbach/gb-ticket-61-symbolic-margin-separator.json
data/open-problem/twin-prime/tp-ticket-61-symbolic-sieve-separator.json
```

Status:

```text
symbolic_failure_offset_open_no_resolution
```

한국어 요약: TICKET-61은 TICKET-60의 가장 큰 약점인 `failure_offset`의 순환성을 제거하는 실험이다. `failure_offset`은 trajectory replay 후에 관측되는 값이므로 그대로는 증명 좌표가 될 수 없다. TICKET-61은 separator key에서 `failure_offset`, `failure_observed`, first-failure certificate를 금지하고, `low40`, certificate prefix length, high-extension bit처럼 replay 전에 알 수 있는 좌표만 사용한다. 결과적으로 mixed 58개 cylinder, 210개 start-template lift에서 `low40 + high_extension mod 16`이 failure offset, observed outcome, boundary prediction label을 모두 결정적으로 분리했다. 이는 증명 경로를 한 단계 강화하지만, 아직 선택된 유한 cylinder 집합 위의 결과다.

English summary: TICKET-61 removes the circular coordinate from TICKET-60. It forbids replay-derived keys and tests whether pre-replay high-extension bits predict the same failure-offset separator. On the selected mixed population, `low40 + high_extension mod 16` is the first joint deterministic pre-replay separator for failure offset, observed outcome, and boundary prediction label. This is not a proof; it is a sharper theorem target.

Key Collatz result:

```text
selected low40 cylinders: 162
selected start-template lifts: 535
mixed cylinders: 58
mixed start-template lifts: 210
low40-only failure-offset collisions: 58 groups / 210 ambiguous rows
low40 + certificate_prefix_length: 36 failure-offset collision groups / 81 ambiguous rows
first mixed pre-replay joint separator: low40_plus_high_extension_mod_2^4
first all-selected pre-replay joint separator: low40_plus_high_extension_mod_2^4
first top-bit joint separator: low40_plus_high_extension_top_6_bits
full proof status: open
```

Discarded route:

```text
Use low40+failure_offset from TICKET60 as if it were a proof coordinate. That is circular because failure_offset is learned only after replaying the trajectory to failure.
```

Candidate theorem still missing:

```text
For every selected mixed low40 cylinder, the mod-16 high-extension residue determines the first failure offset and the boundary prediction label; extend this to a symbolic transition theorem or an automaton-counted cover that excludes full-period nondecreasing cycles.
```

Counterexample target:

```text
A selected or newly lifted mixed cylinder whose failure_offset remains ambiguous under low40 plus high_extension mod 16, or a full-period replay inside a mod-16-separated cylinder.
```

Remaining decisive target:

```text
CO-TICKET-62 Mod16FailureOffsetTransitionOrAutomatonCountedCover
```

Proof boundary:

```text
TICKET-61 does not prove or disprove any of the four open problems. It turns a replay-derived separator into a pre-replay finite-coordinate theorem target, but the infinite symbolic transition theorem remains open.
```

### Ticket 62: Mod16 transition-cover lift audit

CO-TICKET-62 Mod16FailureOffsetTransitionOrAutomatonCountedCover

Artifacts:

```text
data/open-problem/ticket62-mod16-transition-cover-lab.json
data/open-problem/collatz/co-ticket-62-mod16-transition-cover.json
data/open-problem/riemann/rh-ticket-62-transition-closure.json
data/open-problem/goldbach/gb-ticket-62-margin-transition.json
data/open-problem/twin-prime/tp-ticket-62-sieve-transition.json
```

Status:

```text
mod16_transition_cover_open_no_resolution
```

한국어 요약: TICKET-62는 TICKET-61의 pre-replay mod16 좌표가 더 큰 lift에서도 유지되는지 검사한다. 대상은 TICKET-61의 mixed 48비트 start-template row 210개다. 52비트 lift에서는 3,360개 후보 중 55개가 start-template로 남았고, 56비트 lift에서는 53,760개 후보 중 824개가 start-template로 남았다. 두 경우 모두 `low40 + base high_extension mod 16`이 failure offset, observed outcome, boundary prediction label, transition label을 collision 없이 결정했다. full-period replay는 발견되지 않았다. 이는 mod16 automaton-cover 경로를 강화하지만, 아직 유한 lift audit이므로 Collatz 증명은 아니다.

English summary: TICKET-62 tests whether TICKET61's pre-replay mod16 coordinate survives bounded higher lifts. The 52-bit and 56-bit audits find no mod16 collision and no full-period replay among the surviving start-template lifts. This is bounded evidence for a mod16 automaton-cover route, not an infinite theorem.

Key Collatz result:

```text
base mixed cylinders: 58
base mixed start-template lifts: 210
52-bit tested lifts: 3,360
52-bit start-template lifts: 55
52-bit mod16 failure collisions: 0
56-bit tested lifts: 53,760
56-bit start-template lifts: 824
56-bit mod16 failure collisions: 0
full-period escapes: 0
first joint deterministic separator: low40_plus_base_mod16
full proof status: open
```

Discarded route:

```text
Promote TICKET61's mod16 separator directly to an infinite theorem without checking higher-bit lift closure. TICKET62 treats that as an unproved shortcut.
```

Candidate theorem still missing:

```text
For every mixed low40 cylinder and every admissible higher lift, the low40 plus high-extension mod16 state either determines a closed failure-offset transition or enters a finite automaton cover with no full-period nondecreasing cycle.
```

Counterexample target:

```text
A higher start-template lift where low40 plus base mod16 admits two different failure offsets, or a full-period replay inside the tested lift family.
```

Remaining decisive target:

```text
CO-TICKET-63 Mod16AutomatonCoverOrLiftCollision
```

Proof boundary:

```text
TICKET-62 does not prove or disprove any of the four open problems. It tests bounded 52/56-bit lift closure for the mod16 coordinate and finds no collision in that audit, but the infinite symbolic automaton-cover theorem remains open.
```

### Ticket 63: Mod16 automaton-cover table and 60-bit chain audit

CO-TICKET-63 Mod16AutomatonCoverOrLiftCollision

Artifacts:

```text
data/open-problem/ticket63-mod16-automaton-cover-lab.json
data/open-problem/collatz/co-ticket-63-mod16-automaton-cover.json
data/open-problem/riemann/rh-ticket-63-automaton-cover.json
data/open-problem/goldbach/gb-ticket-63-margin-automaton.json
data/open-problem/twin-prime/tp-ticket-63-sieve-automaton.json
```

Status:

```text
mod16_automaton_cover_open_no_resolution
```

한국어 요약: TICKET-63은 TICKET-62의 bounded mod16 transition evidence를 automaton-cover 표로 바꾸는 시도다. 48비트 selected mixed cylinder 58개와 start-template lift 210개에서 출발하고, 56비트 생존 row 824개를 부모 row로 삼아 60비트 targeted chain lift 13,184개를 검사했다. 그 결과 start-template target row 209개가 남았고, 이 row들에 대한 state table은 deterministic이며 collision audit은 0개였다. chained 60비트 row에서 첫 결정적 quotient separator는 `low40 mod 2^20 + base_mod16`이다. 이 결과는 다음 정리 목표를 더 명확히 하지만, finite table audit이므로 콜라츠 증명이나 네 난제의 증명은 아니다.

English summary: TICKET-63 converts TICKET62's bounded mod16 transition evidence into an explicit finite automaton-table audit. It chains the 824 surviving 56-bit rows into 13,184 targeted 60-bit lifts and retains 209 start-template target rows. The resulting state tables are deterministic with no audited automaton collisions and no full-period escape. This sharpens the next theorem target, but it is still a finite audit rather than an infinite proof.

Key Collatz result:

```text
base mixed cylinders: 58
base mixed start-template lifts: 210
56-bit parent survivor rows: 824
60-bit chain tested lifts: 13,184
60-bit start-template chain lifts: 209
60-bit automaton states: 145
automaton collision audits: 0
full-period escapes: 0
first 60-bit quotient separator: low40_mod_2^20_plus_base_mod16
full proof status: open
```

Discarded route:

```text
Treat deterministic 52/56-bit mod16 survival as a proof of Collatz. TICKET63 rejects this route because closure under all higher lifts and all relevant cylinders is still missing.
```

Candidate theorem still missing:

```text
For every admissible lift of the selected mixed-cylinder family, the mod16 state together with the finite quotient low40 mod 2^20 induces a symbolic transition that either stays inside a counted automaton cover with no nondecreasing full-period cycle, or produces an explicit lift collision.
```

Counterexample target:

```text
A higher chained lift or newly admitted mixed cylinder with the same low40 mod 2^20 plus base_mod16 state but conflicting transition label, failure offset, or boundary outcome; alternatively, a full-period replay inside the automaton cover.
```

Remaining decisive target:

```text
CO-TICKET-64 SymbolicMod16AutomatonTransitionProof
```

Proof boundary:

```text
TICKET-63 does not prove or disprove any of the four open problems. It extracts deterministic finite state tables and a stronger quotient separator, but the infinite symbolic transition theorem and any independent formal proof remain open.
```

### Ticket 64: Symbolic mod16 transition gate obstruction

CO-TICKET-64 SymbolicMod16AutomatonTransitionProof

Artifacts:

```text
data/open-problem/ticket64-symbolic-mod16-transition-lab.json
data/open-problem/collatz/co-ticket-64-symbolic-mod16-transition.json
data/open-problem/riemann/rh-ticket-64-gate-predicate.json
data/open-problem/goldbach/gb-ticket-64-cutoff-gate.json
data/open-problem/twin-prime/tp-ticket-64-parity-gate.json
```

Status:

```text
symbolic_mod16_transition_open_no_resolution
```

한국어 요약: TICKET-64는 TICKET-63의 다음 목표였던 `SymbolicMod16AutomatonTransitionProof`를 직접 압박했다. TICKET63에서 얻은 60비트 survivor row 209개 각각에 대해 64비트 후보 자식 16개씩, 총 3,344개를 만들었다. 이 중 start-template child는 42개뿐이고, non-start child는 3,302개였다. 기존 quotient state `low40 mod 2^20 + base_mod16`는 start-template gate를 결정하지 못했다. 같은 state 안에서 start-template/non-start-template이 갈라지는 gate collision group이 42개 나왔다. 더 중요하게, admitted 64비트 child 자체도 더 이상 낙관적 `0->0` 전이를 따르지 않았다. transition label은 `0->1` 20개, `0->2` 11개, `0->3` 5개, `0->5` 3개, `0->4` 3개로 갈라졌다. 따라서 TICKET64는 증명이 아니라, TICKET63의 직접 승격 경로를 반박하고 “symbolic start-template gate + offset-transition relation”을 다음 정리 목표로 만든다.

English summary: TICKET-64 tests the symbolic transition target produced by TICKET63. It extends the 209 retained 60-bit rows to 3,344 candidate 64-bit children. Only 42 are admitted start-template children. The retained quotient state cannot decide the admissibility gate, and the optimistic admitted-child `0->0` transition already fails at 64 bits. This is a useful obstruction to a shortcut, not a proof or counterexample to Collatz.

Key Collatz result:

```text
60-bit parent rows: 209
64-bit candidate children: 3,344
64-bit start-template children: 42
64-bit non-start children: 3,302
state20 gate collision groups: 42
state20+top4 gate collision groups: 24
64-bit admitted transition labels: 0->1:20, 0->2:11, 0->3:5, 0->5:3, 0->4:3
first admitted-child quotient separator: low40_mod_2^16_plus_base_mod16
optimistic 0->0 admitted-child formula: refuted at 64 bits
full proof status: open
```

Discarded route:

```text
Promote the TICKET63 quotient state and the 60-bit 0->0 transition directly to an infinite symbolic theorem. TICKET64 rejects this shortcut because both the next admissibility gate and the admitted-child transition split at 64 bits.
```

Candidate theorem still missing:

```text
For every admissible lift, a symbolic start-template gate first selects the valid children; inside that selected subcover, an explicit offset-transition relation is closed and a well-founded cover excludes full-period nondecreasing cycles.
```

Counterexample target:

```text
A pair of candidate children sharing the refined symbolic gate state but disagreeing on start-template admissibility, or a pair of admitted children sharing the refined transition state but disagreeing on the offset-transition label.
```

Remaining decisive target:

```text
CO-TICKET-65 SymbolicStartTemplateGateAndOffsetTransition
```

Proof boundary:

```text
TICKET-64 does not prove or disprove any of the four open problems. It refutes one overly optimistic finite-to-symbolic promotion path and replaces it with a sharper gate-plus-offset theorem target.
```

### Ticket 65: Start-template chain extinction and gate-compression obstruction

CO-TICKET-65 StartTemplateChainExtinctionOrComplementCover

Artifacts:

```text
data/open-problem/ticket65-start-template-chain-extinction-lab.json
data/open-problem/collatz/co-ticket-65-start-template-chain-extinction.json
data/open-problem/riemann/rh-ticket-65-branch-extinction.json
data/open-problem/goldbach/gb-ticket-65-cutoff-complement.json
data/open-problem/twin-prime/tp-ticket-65-parity-complement.json
```

Status:

```text
start_template_chain_extinction_open_no_resolution
```

한국어 요약: TICKET-65는 TICKET-64가 남긴 `SymbolicStartTemplateGateAndOffsetTransition` 목표를 직접 추적했다. 결과적으로 현재 추적 중인 start-template chain은 `56 bits:824 -> 60 bits:209 -> 64 bits:42 -> 68 bits:12 -> 72 bits:3 -> 76 bits:1 -> 80 bits:0`으로 소멸했다. full-period replay는 0개였다. 따라서 TICKET63/TICKET64에서 가장 강하게 남아 있던 구체 branch는 80비트에서 닫혔다. 그러나 gate separator 탐색은 좋은 소식만은 아니다. 64비트와 68비트에서 결정적 gate는 찾을 수 있지만, 그 결정성은 압축된 symbolic automaton이 아니라 row-unique state로 붕괴한다. 즉 이 결과는 “현재 branch closure”이지 “전역 Collatz proof”가 아니다.

English summary: TICKET-65 follows the retained TICKET63/TICKET64 start-template chain until it becomes extinct at 80 bits. This is strong branch pruning, but not a global theorem. The audit also shows that the deterministic gate separators found at 64 and 68 bits are row-unique, so the compact finite-automaton route remains blocked.

Key Collatz result:

```text
survivor sequence: 824 -> 209 -> 42 -> 12 -> 3 -> 1 -> 0
extinction at bits: 80
full-period replays: 0
64-bit best compressed near miss: low40_parent_high10_child_top4, 3 collision groups, 6 ambiguous rows
64-bit first deterministic gate: low40_parent_top_parent_high10_child_top4, row-unique
68-bit best compressed near miss: low40_parent_high2_child_top4, 1 collision group, 2 ambiguous rows
68-bit first deterministic gate: state20_base_mod16_child_top4, row-unique
full proof status: open
```

Discarded route:

```text
Treat the TICKET63/TICKET64 start-template survivor chain as a compact repeating automaton. TICKET65 closes that concrete chain by 80 bits and shows that the deterministic gate keys are row-unique rather than compressed.
```

Candidate theorem still missing:

```text
StartTemplateChainExtinctionOrComplementCover: every branch in the current start-template cover either exits the cover in finite symbolic time or is captured by a non-row-unique gate predicate with a well-founded offset transition.
```

Counterexample target:

```text
A 4-bit lift branch beyond the current cover that re-enters a start-template lasso with a repeated non-row-unique gate state, or a compact gate separator that remains deterministic beyond the 80-bit extinction audit.
```

Remaining decisive target:

```text
CO-TICKET-66 ComplementCoverForStartTemplateExit
```

Proof boundary:

```text
TICKET-65 does not prove or disprove any of the four open problems. It closes one tracked Collatz branch, but it does not prove that every integer enters that branch or that every branch leaving it descends.
```

### Ticket 66: Complement-cover audit and open-template frontier

CO-TICKET-66 ComplementCoverForStartTemplateExit

Artifacts:

```text
data/open-problem/ticket66-complement-cover-lab.json
data/open-problem/collatz/co-ticket-66-complement-cover.json
data/open-problem/riemann/rh-ticket-66-complement-cover.json
data/open-problem/goldbach/gb-ticket-66-complement-cover.json
data/open-problem/twin-prime/tp-ticket-66-complement-cover.json
```

Status:

```text
complement_cover_open_no_resolution
```

한국어 요약: TICKET-66은 TICKET-65가 요구한 보완 덮개 정리를 직접 검사한다. TICKET-65에서 추적한 start-template chain은 80비트에서 닫혔지만, 그것만으로는 전역 Collatz 증명이 되지 않는다. 따라서 모든 non-start-template exit branch가 이미 descent/terminal machinery로 닫히는지 확인해야 한다. 계산 결과는 부정적이다. 56->60, 60->64, 64->68, 68->72, 72->76, 76->80 lift에서 나온 non-start-template 후보는 총 17,189개이고, 그중 55개만 즉시 all-lift descent로 닫힌다. 나머지 17,134개는 491개 열린 `needs_split` template family로 남는다. 이는 “보완 덮개가 이미 있다”는 지름길을 반박하고, 다음 표적을 열린 template family rank theorem 또는 실제 무한 lift 반례 후보로 좁힌다.

English summary: TICKET-66 audits the complement theorem required after TICKET-65. The result is not a proof. It refutes the shortcut that every branch outside the tracked start-template chain is already covered by existing descent or terminal-family arguments. The next decisive object is a rank theorem over the 491 open template families, or a compatible infinite lift through one of them.

Key Collatz result:

```text
non-start complement candidates: 17,189
closed by immediate all-lift descent: 55
open needs_split instances: 17,134
descent coverage rate: 0.003199720752
unique open template families: 491
largest open family: [12,[1,1,1,1],103,5] with 432 instances
exit pressure: open_wrong_tail_target_residue_mod_256 = 14,244; open_target_tail_wrong_next_valuation = 2,890
full proof status: open
```

Discarded route:

```text
Assume that every branch leaving the TICKET65 start-template chain is already handled by the existing descent or terminal-family closures. TICKET66 refutes that shortcut: only 55 of 17,189 complement candidates close by immediate all-lift descent.
```

Candidate theorem still missing:

```text
OpenTemplateFamilyRankOrComplementCounterexample: every open template family left by ComplementCoverForStartTemplateExit admits a well-founded symbolic rank after a finite split, or there exists a compatible infinite lift preserving one nondecreasing template family.
```

Counterexample target:

```text
A compatible infinite lift through one of the 491 open complement template families, starting with the smallest open residue or one of the largest families such as [12,[1,1,1,1],103,5].
```

Remaining decisive target:

```text
CO-TICKET-67 OpenTemplateFamilyRankOrComplementCounterexample
```

Proof boundary:

```text
TICKET-66 does not prove or disprove any of the four open problems. It narrows the next Collatz proof/counterexample frontier to 491 open complement template families and explicitly blocks the claim that the TICKET-65 complement was already covered.
```

### Ticket 67: Open-template rank audit and cyclic frontier extraction

CO-TICKET-67 OpenTemplateFamilyRankOrComplementCounterexample

Artifacts:

```text
data/open-problem/ticket67-open-template-rank-lab.json
data/open-problem/collatz/co-ticket-67-open-template-rank.json
data/open-problem/riemann/rh-ticket-67-rank-cycle-frontier.json
data/open-problem/goldbach/gb-ticket-67-rank-cycle-frontier.json
data/open-problem/twin-prime/tp-ticket-67-rank-cycle-frontier.json
```

Status:

```text
rank_cycle_frontier_open_no_resolution
```

한국어 요약: TICKET-67은 TICKET-66에서 남은 491개 열린 template family를 한 단계 더 공격한다. 각 열린 source instance를 4비트 더 lift하여 16개 child를 검사했고, 총 274,144개 child lift를 만들었다. 결과는 단순 rank route에 부정적이다. 17,134개 source instance 중 모든 child가 닫힌 것은 13개뿐이고, 17,121개는 계속 열린 child를 가진다. child 상태는 `needs_split = 265,812`, `all_lift_descent = 8,332`이다. open transition graph는 45,665개의 distinct edge와 265,812 edge weight를 가지며, 5,100개 node 중 429개 node가 하나의 cyclic SCC를 이룬다. source family 458개가 이 cycle에 도달한다. 또한 scalar debt rank도 실패한다. open child transition 중 96,433개가 debt를 감소시키지 않는다. 따라서 다음 정리는 단순 template rank가 아니라 429-node SCC를 더 세밀한 pre-replay coordinate로 분해하거나, 그 SCC 안에 무한히 머무는 compatible lift가 불가능함을 보여야 한다.

English summary: TICKET-67 tests whether TICKET66's 491 open families close after one more 4-bit split or admit a simple rank. Both shortcuts fail. The finite quotient has a 429-node cyclic SCC and many nondecreasing debt edges. This is not a counterexample; it is a precise finite obstruction that must be refined or ruled out by an infinite compatibility theorem.

Key Collatz result:

```text
source open instances: 17,134
source open template families: 491
child lift rows: 274,144
child needs_split: 265,812
child all_lift_descent: 8,332
source instances closed after one split: 13
source instances still open after one split: 17,121
open transition edge count: 45,665
open transition edge weight: 265,812
transition nodes: 5,100
child open template families: 5,056
cyclic components: 1
cyclic nodes: 429
largest cyclic component: 429
cycle edge weight: 89,222
source families reaching cycle: 458
debt nondecreasing edges: 96,433
debt nondecreasing rate: 0.362786480671
full proof status: open
```

Discarded route:

```text
Try to close the 491 open template families by one 4-bit split or by a scalar debt rank. TICKET67 refutes both shortcuts: 17,121 of 17,134 source instances still have open children, the template graph has a large cyclic component, and many open child transitions do not decrease debt.
```

Candidate theorem still missing:

```text
CycleSCCRefinementOrInfiniteLiftExclusion: every edge inside the TICKET67 cyclic template SCC either exits under a finite pre-replay coordinate refinement with a well-founded rank, or no compatible infinite 2-adic lift can follow the SCC forever.
```

Counterexample target:

```text
A compatible infinite lift that stays inside the 429-node cyclic template SCC while avoiding all descent closures. The TICKET67 SCC is only a quotient-cycle candidate, not a Collatz counterexample.
```

Remaining decisive target:

```text
CO-TICKET-68 CycleSCCRefinementOrInfiniteLiftExclusion
```

Proof boundary:

```text
TICKET-67 does not prove or disprove any of the four open problems. It refutes two simpler rank routes and isolates a finite quotient-cycle obstruction that still requires an infinite compatibility theorem.
```

### Ticket 68: Cycle-SCC refinement and bounded DAG extraction

CO-TICKET-68 CycleSCCRefinementOrInfiniteLiftExclusion

Artifacts:

```text
data/open-problem/ticket68-cycle-scc-refinement-lab.json
data/open-problem/collatz/co-ticket-68-cycle-scc-refinement.json
data/open-problem/riemann/rh-ticket-68-frontier-refinement.json
data/open-problem/goldbach/gb-ticket-68-frontier-refinement.json
data/open-problem/twin-prime/tp-ticket-68-frontier-refinement.json
```

Status:

```text
cycle_scc_refined_open_no_resolution
```

한국어 요약: TICKET-68은 TICKET-67에서 나온 429-node cyclic SCC를 실제 반례 후보처럼 취급하지 않고, 더 세밀한 pre-replay coordinate로 다시 분해한다. 총 7개 refinement family를 시험했다. `base_template` 좌표에서는 429개 cyclic node와 89,222 cycle edge weight가 그대로 남는다. 그러나 `base_template + prefix_length + consumed_bits` 좌표를 추가하면 관측된 SCC 내부 transition graph가 9,616개 state, 41,283개 edge의 DAG로 깨지고 cyclic node는 0개가 된다. 더 약한 tail/residue-only refinement 중 가장 강한 `tail8_res4096_vexact`도 cyclic node를 429개에서 26개, cyclic edge weight를 89,222에서 129로 줄인다. 이 결과는 증명이 아니다. 하지만 TICKET-67의 순환이 피할 수 없는 구조라는 해석은 버려야 하며, 다음 증명 목표는 prefix/consumed DAG가 모든 compatible higher lift에 대해 transition-complete인지 증명하는 것이다.

English summary: TICKET-68 refines the TICKET67 429-node quotient cycle instead of treating it as a counterexample. The observed cycle disappears under the `base_prefix_consumed` coordinate: 9,616 refined states, 41,283 refined edges, zero cyclic nodes, and observed topological rank 5. Tail/residue-only refinement still leaves 26 cyclic nodes, so the missing theorem is not merely "more residue bits"; it is a transition-completeness and well-foundedness theorem for the prefix/consumed DAG.

Key Collatz result:

```text
source base transition nodes: 5,100
source base transition edges: 45,665
source base transition weight: 265,812
source cyclic nodes: 429
source cycle edge weight: 89,222
open exits from cycle: 174,589
tested refinement families: 7
strongest acyclic refinement: base_prefix_consumed
base_prefix_consumed states: 9,616
base_prefix_consumed edges: 41,283
base_prefix_consumed cyclic nodes: 0
base_prefix_consumed observed topological rank: 5
best tail/residue-only refinement: tail8_res4096_vexact
tail8_res4096_vexact cyclic nodes: 26
tail8_res4096_vexact cyclic edge weight: 129
full proof status: open
```

Discarded route:

```text
Treat the 429-node TICKET67 cycle as an unavoidable obstruction at every finite refinement. TICKET68 refutes that overstatement on the observed transition set: adding prefix_length and consumed_bits makes the observed internal cycle graph acyclic.
```

Candidate theorem still missing:

```text
PrefixConsumedDAGCompletenessOrPersistentRefinedCycle: every compatible lift inside the TICKET67 SCC is represented by the base_template + prefix_length + consumed_bits refined transition system and decreases its observed DAG rank, or a new persistent refined cycle appears at a higher lift.
```

Counterexample target:

```text
A compatible infinite 2-adic lift whose refined state either escapes the observed prefix/consumed DAG completeness conditions or creates a new refined cycle beyond the current bounded horizon.
```

Remaining decisive target:

```text
CO-TICKET-69 PrefixConsumedDAGCompletenessOrPersistentRefinedCycle
```

Proof boundary:

```text
TICKET-68 does not prove or disprove any of the four open problems. It breaks the observed TICKET67 SCC under a stronger coordinate, but the missing infinite bridge is transition-completeness and well-foundedness for all higher lifts.
```

### Ticket 69: Prefix/consumed rank certificate and frontier audit

CO-TICKET-69 PrefixConsumedDAGCompletenessOrPersistentRefinedCycle

Artifacts:

```text
data/open-problem/ticket69-prefix-consumed-rank-lab.json
data/open-problem/collatz/co-ticket-69-prefix-consumed-rank.json
data/open-problem/riemann/rh-ticket-69-rank-completeness.json
data/open-problem/goldbach/gb-ticket-69-rank-completeness.json
data/open-problem/twin-prime/tp-ticket-69-rank-completeness.json
```

Status:

```text
prefix_consumed_rank_frontier_open_no_resolution
```

한국어 요약: TICKET-69는 TICKET-68의 prefix/consumed DAG를 실제 rank certificate 후보로 검사한다. 결과는 양면적이다. 관측된 내부 edge 89,222개는 모두 rank를 엄격히 감소시킨다. nondecreasing rank edge는 0개이며, rank delta는 1부터 5까지 모두 양수다. 또한 base-cycle source instance 16,967개에서 child는 `internal_rank_descent = 89,222`, `open_base_cycle_exit = 174,589`, `closed_or_terminal_all_lift_descent = 7,661`로 분류된다. 그러나 이 결과는 아직 증명이 아니다. rank 0 상태 6,733개 중 6,649개는 child-only unexpanded frontier로 남는다. 즉 현재 DAG는 관측 내부 edge에 대해서는 rank이지만, 그 frontier의 다음 transition-completeness가 아직 없다.

English summary: TICKET-69 turns the TICKET68 acyclic graph into a stricter rank certificate candidate. All 89,222 observed internal edges strictly decrease the prefix/consumed rank, and there are zero nondecreasing rank edges. The blocking issue is not local rank descent anymore; it is transition-completeness of the frontier. There are 6,649 rank-0 child-only states that still need expansion or theorem-level closure.

Key Collatz result:

```text
coordinate family: base_prefix_consumed
rank states: 9,616
max rank: 5
source base cycle nodes: 429
observed internal edge weight: 89,222
nondecreasing rank edges: 0
source instances in base cycle: 16,967
child outcomes: internal_rank_descent = 89,222; open_base_cycle_exit = 174,589; closed_or_terminal_all_lift_descent = 7,661
source-expanded states: 3,025
source-and-child states: 1,390
source-only states: 1,635
child-only unexpanded states: 6,649
unexpanded child-only rank counts: rank 0 = 6,649
full proof status: open
```

Discarded route:

```text
Promote the observed prefix/consumed DAG directly to a proof. TICKET69 blocks that shortcut: the internal observed edges strictly decrease the DAG rank, but many child-only refined states have not yet been expanded as source states.
```

Candidate theorem still missing:

```text
PrefixConsumedRankCompleteness: every compatible branch represented by a TICKET68 child-only prefix/consumed state has a complete next-transition expansion whose internal children strictly decrease the same DAG rank, or a new refined cycle is produced.
```

Counterexample target:

```text
A higher-lift expansion of an unexpanded child-only prefix/consumed state that re-enters a nondecreasing refined cycle.
```

Remaining decisive target:

```text
CO-TICKET-70 PrefixConsumedFrontierExpansionOrCycle
```

Proof boundary:

```text
TICKET-69 does not prove or disprove any of the four open problems. It validates strict rank descent on observed internal edges, but the unexpanded child-only frontier is the missing infinite bridge.
```

### Ticket 70: Prefix/consumed frontier expansion and direct-rank closure refutation

CO-TICKET-70 PrefixConsumedFrontierExpansionOrCycle

Artifacts:

```text
data/open-problem/ticket70-prefix-frontier-expansion-lab.json
data/open-problem/collatz/co-ticket-70-prefix-frontier-expansion.json
data/open-problem/riemann/rh-ticket-70-frontier-expansion.json
data/open-problem/goldbach/gb-ticket-70-frontier-expansion.json
data/open-problem/twin-prime/tp-ticket-70-frontier-expansion.json
```

Status:

```text
prefix_frontier_expansion_open_no_resolution
```

한국어 요약: TICKET-70은 TICKET-69가 남긴 rank-0 child-only frontier를 실제로 한 단계 확장한다. 기준은 TICKET-69와 동일하다. frontier state는 6,649개이고, 그 state에 도달한 concrete representative는 49,504개다. 각 representative에 4비트 child 16개를 붙여 총 792,064개 branch를 검사했다. 결론은 직접 rank closure의 반박이다. 516,176개 branch는 base cycle 밖으로 exit하고 61,118개는 all-lift descent로 닫히지만, 123,403개는 rank 0으로 재진입하고 31,918개는 rank 1 이상으로 올라간다. 또한 59,449개 branch는 기존 DAG에 없던 unranked internal state로 들어간다. 따라서 "TICKET69 rank-0 sink는 자동 terminal"이라는 shortcut은 버려야 한다.

English summary: TICKET-70 expands the TICKET69 rank-0 child-only frontier by one 4-bit lift. It does not find a combined refined cycle in this one-step audit, but it refutes the direct rank-0 closure shortcut. The expanded frontier has 155,321 known-rank nondecreasing re-entry edges, 59,449 new unranked internal edges, and 3,537 representative-nondeterministic frontier states.

Key Collatz result:

```text
coordinate family: base_prefix_consumed
source frontier states: 6,649
frontier concrete representatives: 49,504
expansion edge weight: 792,064
frontier internal edge weight: 214,770
open base-cycle exits: 516,176
closed all-lift descent branches: 61,118
known-rank nondecreasing re-entry edges: 155,321
  rank-equal re-entry edges: 123,403
  rank-increase re-entry edges: 31,918
new unranked internal edges: 59,449
representative-nondeterministic frontier states: 3,537
combined one-step cycle components: 0
full proof status: open
```

Discarded route:

```text
Treat every TICKET69 rank-0 child-only state as a terminal sink. TICKET70 directly refutes this route: many concrete representatives re-enter ranked or new unranked internal states after one 4-bit expansion.
```

Retained route:

```text
The next useful theorem must add a stronger frontier coordinate, or prove that nondecreasing re-entry pressure cannot persist along compatible infinite lifts. If persistence is possible, extract it as a refined counterexample target.
```

Candidate theorem still missing:

```text
StrongerFrontierCoordinateOrPersistentLiftCycle: every compatible expansion of a TICKET70 rank-0 frontier state is separated by a pre-replay coordinate that supplies a well-founded rank, or it admits a compatible infinite lift cycle/re-entry chain.
```

Counterexample target:

```text
A compatible higher-lift path that starts in one of the rank-0 child-only prefix/consumed states and repeatedly re-enters known ranked or new unranked internal states without descent.
```

Remaining decisive target:

```text
CO-TICKET-71 StrongerFrontierCoordinateOrPersistentLiftCycle
```

Proof boundary:

```text
TICKET-70 does not prove or disprove any of the four open problems. It refutes a direct frontier-closure shortcut and narrows the next target to a stronger coordinate or a persistent lift-cycle extraction.
```

### Ticket 71: Stronger frontier coordinates and bounded separator tradeoff

CO-TICKET-71 StrongerFrontierCoordinateOrPersistentLiftCycle

Artifacts:

```text
data/open-problem/ticket71-stronger-frontier-coordinate-lab.json
data/open-problem/collatz/co-ticket-71-stronger-frontier-coordinate.json
data/open-problem/riemann/rh-ticket-71-stronger-frontier-coordinate.json
data/open-problem/goldbach/gb-ticket-71-stronger-frontier-coordinate.json
data/open-problem/twin-prime/tp-ticket-71-stronger-frontier-coordinate.json
```

Status:

```text
stronger_frontier_coordinate_open_no_resolution
```

한국어 요약: TICKET-71은 TICKET-70의 재진입 압력을 outcome label 없이 분리할 수 있는지 검사한다. 시험한 좌표는 `base_prefix_consumed`, residue mod `2^12`, residue mod `2^16`, tail8+residue, tail12+residue, full valuation word+residue mod `2^16`이다. 결과는 tradeoff다. compact한 `base_prefix_consumed`는 expanded graph를 acyclic하게 유지하고 rank 7을 만들며 child-only frontier를 8,055개로 가장 작게 유지한다. 하지만 mixed transition key가 22,219개 남는다. 반대로 `base_fullword_residue65536`은 bounded transition key를 완전히 분리해서 mixed key 0개를 만든다. 그러나 state count가 319,801개, child-only frontier가 254,488개로 폭증한다. 따라서 "분리 가능한 좌표가 있다"와 "증명 가능한 compact invariant가 있다"는 같은 말이 아니다.

English summary: TICKET-71 finds a bounded separator but not a proof. The full valuation-word plus residue mod `2^16` coordinate gives zero mixed transition keys across the TICKET70 branch set, but it overfits the bounded data and expands the child-only frontier. The compact baseline coordinate keeps the expanded graph small and acyclic, but leaves mixed transition keys. The next proof target is an infinite lift-closure theorem for a compact coordinate, or a persistent lift-chain counterexample target extracted from the remaining mixed keys.

Key Collatz result:

```text
frontier source states: 6,649
frontier concrete representatives: 49,504
frontier branch weight: 792,064
pressure rows: 214,770
tested coordinate families: 6
best bounded transition separator: base_fullword_residue65536
best separator mixed transition keys: 0
best separator transition keys: 792,064
best separator child-only frontier: 254,488
best compact frontier reduction: base_prefix_consumed
compact expanded graph rank: 7
compact child-only frontier after expansion: 8,055
compact mixed transition keys: 22,219
full proof status: open
```

Discarded route:

```text
Treat a large full-word separator as a Collatz proof. TICKET71 blocks that shortcut: the coordinate separates the bounded branch set but explodes the frontier and still has no infinite lift-closure theorem.
```

Retained route:

```text
Either prove that a compact coordinate such as base_prefix_consumed has horizon-independent lift closure after frontier expansion, or extract a persistent lift chain from the mixed transition keys that survive compact coordinates.
```

Candidate theorem still missing:

```text
InfiniteFrontierCoordinateLiftClosureOrChain: every compatible future lift of the expanded frontier is closed by a compact pre-outcome coordinate with a well-founded rank, or there exists a compatible infinite chain through a mixed transition key.
```

Counterexample target:

```text
A repeated lift chain through a mixed transition key or child-only expanded state that survives every tested low-residue and valuation-word coordinate without descent.
```

Remaining decisive target:

```text
CO-TICKET-72 InfiniteFrontierCoordinateLiftClosureOrChain
```

Proof boundary:

```text
TICKET-71 does not prove or disprove any of the four open problems. It identifies a bounded coordinate separator and a compact-coordinate obstruction; the infinite lift theorem remains missing.
```

### Ticket 72: Infinite-frontier lift closure and persistent mixed-key pressure

CO-TICKET-72 InfiniteFrontierCoordinateLiftClosureOrChain

Artifacts:

```text
data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json
data/open-problem/collatz/co-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/riemann/rh-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/goldbach/gb-ticket-72-infinite-frontier-lift-closure.json
data/open-problem/twin-prime/tp-ticket-72-infinite-frontier-lift-closure.json
```

Status:

```text
infinite_frontier_lift_closure_open_no_resolution
```

한국어 요약: TICKET-72는 TICKET-71의 남은 compact mixed key가 단순한 1단계 관측 착시인지, 아니면 lift를 해도 계속 남는 구조적 압력인지 검사한다. 중요한 논리 수정은 `pressure_rank_descent`를 열린 압력에서 제외한 점이다. rank가 내려가는 branch는 증명 관점에서 진전이므로, 열린 압력은 `pressure_rank_equal`, `pressure_rank_increase`, `pressure_new_unranked_internal`만으로 다시 센다. 이 보수적 기준에서도 TICKET70 frontier branch weight 792,064, compact mixed transition key 22,219개, open-pressure mixed transition key 20,752개가 재구성된다. 상위 8개 compact mixed key를 한 단계 lift하면 36,848개 second-layer row가 나오고, 그중 6,857개가 open pressure이며, 4,142개가 open-pressure mixed-key로 재진입한다. 2,048개 source에 대한 제한된 third probe에서도 32,768개 row 중 12,300개 open pressure와 6,448개 open-pressure mixed-key 재진입이 남는다. `base_tail12_residue65536`은 가장 좋은 compact 후보지만 mixed key 540개를 남기고, `base_fullword_residue65536`은 mixed key 0개를 만들지만 overfit guard로만 남는다.

English summary: TICKET-72 does not solve Collatz. It refines the TICKET71 obstruction by separating rank descent from open pressure, then lifting the top compact mixed transition keys. The result is persistent bounded pressure: open-pressure mixed-key re-entry survives the second lift and a capped third probe. This strengthens the next target from "try a bigger coordinate" to a sharper dichotomy: prove a compact mixed-key invariant under all future lifts, or extract a compatible persistent lift chain.

Key Collatz result:

```text
reconstructed frontier branch weight: 792,064
compact mixed transition keys: 22,219
compact open-pressure mixed transition keys: 20,752
selected top mixed keys: 8
first-layer rows selected: 2,512
first-layer pressure rows selected: 2,303
second-layer rows: 36,848
second-layer open-pressure rows: 6,857
second-layer rank-descent rows: 2,021
second-layer mixed-key re-entries: 9,584
second-layer open-pressure mixed-key re-entries: 4,142
third-probe sources: 2,048
third-probe rows: 32,768
third-probe open-pressure rows: 12,300
third-probe rank-descent rows: 342
third-probe mixed-key re-entries: 11,455
third-probe open-pressure mixed-key re-entries: 6,448
best compact candidate: base_tail12_residue65536, 540 mixed keys
bounded overfit guard: base_fullword_residue65536, 0 mixed keys
full proof status: open
```

Discarded route:

```text
Treat rank descent as proof pressure, or treat a full valuation word as a compact invariant. TICKET72 blocks both shortcuts: rank descent is progress, not an obstruction, while the full-word coordinate closes only the bounded rows and has no compact infinite transition theorem.
```

Retained route:

```text
Prove that a compact coordinate such as base_tail12_residue65536 has horizon-independent mixed-key closure, or extract a persistent compatible lift chain from the open-pressure mixed-key re-entries.
```

Candidate theorem still missing:

```text
CompactMixedKeyInvariantOrPersistentLiftChain: every compatible future lift of the TICKET72 compact mixed-key frontier is controlled by a finite pre-outcome coordinate with well-founded descent, or there exists a compatible infinite chain that repeatedly re-enters open-pressure mixed keys.
```

Counterexample target:

```text
A compatible infinite lift chain whose every finite prefix survives the compact coordinates and whose transition profile repeatedly enters pressure_rank_equal, pressure_rank_increase, or pressure_new_unranked_internal without a well-founded descent certificate.
```

Remaining decisive target:

```text
CO-TICKET-73 CompactMixedKeyInvariantOrPersistentLiftChain
```

Proof boundary:

```text
TICKET-72 does not prove or disprove any of the four open problems. It only shows that the compact mixed-key obstruction persists under the tested second and third lifts, so an independently checkable infinite theorem or certified counterexample is still required.
```

### Ticket 73: Lineage-constrained strict re-entry tree

CO-TICKET-73 FiniteRootReentryTreeExtinctionOrKonigWitness

Artifacts:

```text
data/open-problem/ticket73-lineage-pressure-forest-lab.json
data/open-problem/collatz/co-ticket-73-lineage-pressure-forest.json
data/open-problem/riemann/rh-ticket-73-lineage-pressure-forest.json
data/open-problem/goldbach/gb-ticket-73-lineage-pressure-forest.json
data/open-problem/twin-prime/tp-ticket-73-lineage-pressure-forest.json
```

Status:

```text
strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion
```

한국어 요약: TICKET-73은 TICKET-72의 4,142개 open-pressure mixed-key 재진입 row 전체를 root로 삼아, 이전의 2,048개 제한 third probe를 제거했다. 각 root의 자식은 4비트 상위 확장 16개를 모두 정확히 열거하고, 자식 residue가 부모 residue를 mod `2^parent_bits`에서 보존하는지 검사했다. third lift 66,272개 row 중 strict 재진입은 12,911개(1,835개 root), fourth lift 206,576개 row 중 2,873개(614개 root)였다. 이 2,873개를 다시 전부 열어 fifth lift 45,968개를 검사했을 때 strict 재진입은 0개였다. 따라서 선택된 finite root 집합에서 “매 lift마다 open pressure이면서 원래 compact mixed-key로 재진입”하는 무한 사슬은 없다. 이 유한 소거는 Collatz 전체에 대한 결론이 아니다. root가 모든 미해결 Collatz 궤적을 덮는다는 coverage 정리가 없고, strict predicate 밖의 압력 사슬도 배제하지 않았기 때문이다.

English summary: TICKET-73 removes the TICKET-72 third-probe cap by using all 4,142 open-pressure mixed-key re-entry rows as roots. It enumerates all sixteen exact four-bit congruence extensions at each retained node and checks parent-child residue compatibility. The all-root third lift has 66,272 rows with 12,911 strict re-entries across 1,835 roots; the fourth lift has 206,576 rows with 2,873 strict re-entries across 614 roots; the fifth lift has 45,968 rows with zero strict re-entries. Hence no infinite chain through this selected finite root set can satisfy the strict condition of open pressure plus re-entry to the original compact mixed-key predicate at every lift. This is a finite elimination of one counterexample route, not a Collatz proof: no coverage theorem connects these roots to every unresolved trajectory, and other pressure predicates remain possible.

Exact finite result:

```text
selected strict roots: 4,142
third lift:  66,272 rows, 12,911 strict re-entries, 1,835 surviving roots
fourth lift: 206,576 rows, 2,873 strict re-entries, 614 surviving roots
fifth lift:  45,968 rows, 0 strict re-entries, 0 surviving roots

bounded lemma: the selected strict re-entry tree is empty at the fifth retained lift.
```

Discarded route:

```text
Treat the TICKET72 repeated re-entry counts as evidence for an infinite chain. The all-root strict tree is exactly empty at its fifth retained lift, so that particular persistent-chain specification cannot supply a Collatz counterexample.
```

Retained route:

```text
Either prove that a theorem-level coverage certificate reduces every unresolved Collatz trajectory to a finite collection of exactly exhaustible root trees, or define a different pressure predicate and prove nonempty compatible descendants at every depth before invoking Konig's lemma.
```

Candidate theorem still missing:

```text
CoverageCertificateAndAllDepthReentryTreeDecision: every unresolved Collatz trajectory is covered by a finite, exact congruence-root family whose admissible pressure tree either becomes empty at a finite lift or is nonempty at every depth; only the latter permits an infinite compatible path by Konig's lemma, and an additional dynamical argument is required to turn that path into a counterexample.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
Bounded survivors are not theorem candidates until their frontier coverage, lineage compatibility, and all-scale decision rule are separately established. Ticket 73 records those obligations on all four pages but transfers no Collatz counts to the other problems.
```

Proof boundary:

```text
TICKET-73 does not prove or disprove any of the four open problems. It proves only a finite extinction statement for a precisely selected Collatz re-entry predicate and leaves the global coverage and infinite-theorem obligations open.
```

### Ticket 74: Coverage leakage and escaping-pressure forest

CO-TICKET-74 FiniteRootCoverageLeakageOrEscapingPressureForest

Artifacts:

```text
data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json
data/open-problem/collatz/co-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/riemann/rh-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/goldbach/gb-ticket-74-coverage-leakage-escape-forest.json
data/open-problem/twin-prime/tp-ticket-74-coverage-leakage-escape-forest.json
```

Status:

```text
strict_cover_leakage_and_sixth_pressure_persistence_observed_no_global_resolution
```

한국어 요약: TICKET-74는 TICKET-73의 strict 재진입 트리 소거가 전체 pressure closure인지 검사한다. 결론은 아니다. TICKET73의 4,142개 root는 T70의 open-pressure mixed key 20,752개 중 상위 8개에서 나온다. key 기준 coverage는 `8 / 20,752 = 0.038551%`, first-layer row 기준은 `2,512 / 371,343 = 0.676464%`, first-layer open-pressure row 기준은 `2,303 / 180,385 = 1.276714%`다. strict tree의 fifth lift는 열린 압력 15,696개를 남기지만, 기존 compact mixed-key cover 재진입은 0개다. 그중 15,593개(99.343782%)가 새 `pressure_new_unranked_internal` 상태로 빠져나간다. 이 escape 15,696개를 전부 sixth lift로 확장하면 251,136개 row 중 열린 압력 78,315개가 남고, 기존 cover 재진입은 5개뿐이다. 따라서 strict predicate의 유한 소거는 전역 pressure 소거나 전역 coverage 정리가 아니다.

English summary: TICKET-74 tests whether the TICKET-73 strict re-entry-tree extinction is actual pressure closure. It is not. The 4,142 TICKET73 roots arise from only the top 8 of 20,752 T70 open-pressure mixed keys: `8 / 20,752 = 0.038551%` by key, `2,512 / 371,343 = 0.676464%` by first-layer row, and `2,303 / 180,385 = 1.276714%` by first-layer open-pressure row. The strict tree's fifth lift leaves 15,696 open-pressure rows but zero re-entries to the original compact mixed-key cover; 15,593 rows (99.343782%) enter new unranked internal states. Expanding all 15,696 escapes produces 251,136 sixth-lift rows with 78,315 open-pressure rows and only 5 old-cover re-entries. Strict-predicate extinction is therefore not global pressure extinction or a coverage theorem.

Exact coverage and leakage result:

```text
T70 open-pressure mixed keys: 20,752
TICKET73 selected keys: 8 (0.038551%)
selected first-layer rows: 2,512 / 371,343 (0.676464%)
selected first-layer open-pressure rows: 2,303 / 180,385 (1.276714%)

fifth lift: 45,968 exact rows, 15,696 open pressure, 0 old-cover re-entries,
             15,593 new unranked internal states, 0 extension-compatibility failures
sixth lift: 251,136 exact rows, 78,315 open pressure, 5 old-cover re-entries,
             78,315 new unranked internal states, 0 extension-compatibility failures
```

Discarded route:

```text
Infer global Collatz closure from the TICKET73 strict-tree extinction. TICKET74 gives an exact counterexample to that inference: the old compact cover does not contain the fifth-lift open-pressure successors.
```

Retained route:

```text
Prove a horizon-independent global coverage certificate for every escaping needs_split state, or define a larger pressure predicate whose exact compatible forest can be shown empty at finite depth or nonempty at every depth.
```

Candidate theorem still missing:

```text
GlobalCoverageCertificateOrEscapingPressureForestDecision: every unresolved Collatz trajectory is covered by a fixed, exact congruence-state family with a well-founded descent coordinate, or every escaping successor belongs to a precisely defined pressure forest whose all-depth compatible paths are decided. Any surviving path still requires a separate proof that it represents divergence or a nontrivial cycle.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
Every bounded zero, exceptional-even, or exact-gap frontier must prove successor closure under its claimed cover. A bounded extinction result that merely leaks to untracked states is not a theorem for any of the four problems.
```

Proof boundary:

```text
TICKET-74 does not prove or disprove any of the four open problems. It refutes one invalid globalization step, records an exact escaping-pressure forest through the sixth lift, and leaves the required global coverage theorem open.
```

### Ticket 75: Fixed finite coordinate closure audit

CO-TICKET-75 EscapeCoordinateClosureOrNovelClassGrowth

Artifacts:

```text
data/open-problem/ticket75-escape-coordinate-closure-lab.json
data/open-problem/collatz/co-ticket-75-escape-coordinate-closure.json
data/open-problem/riemann/rh-ticket-75-escape-coordinate-closure.json
data/open-problem/goldbach/gb-ticket-75-escape-coordinate-closure.json
data/open-problem/twin-prime/tp-ticket-75-escape-coordinate-closure.json
```

Status:

```text
all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution
```

한국어 요약: TICKET-75는 TICKET-74의 fifth-lift 열린 압력 15,696개와 sixth-lift 열린 압력 78,315개를 exact congruence extension 실패 0개로 다시 재생했다. 기존 `base_prefix_consumed` DAG 좌표는 exact `prefix_length`와 `consumed_bits`를 포함하므로 고정 유한 상태가 아니라는 점을 명시적으로 강등했다. 대신 valuation tail, low residue, clipped next valuation, prefix/consumed modular data만 사용하는 고정 유한 pre-outcome 좌표 8개를 시험했다. 어느 좌표도 관측된 successor closure, projected-cycle exclusion, pressure-outcome determinism을 동시에 통과하지 못했다. 가장 거친 좌표는 새 sixth row가 `11 / 78,315`뿐이지만 cyclic node 66개와 mixed key 59개를 남겼다. 가장 세밀한 좌표는 mixed key를 4개까지 줄였지만 `77,998 / 78,315` row가 관측 source cover 밖의 새 class로 빠졌다. 이것은 시험한 coordinate grammar의 압축-상태성장 trade-off이며 Collatz 전체에 관한 정리가 아니다.

English summary: TICKET-75 exactly replays all 15,696 fifth-lift and 78,315 sixth-lift open-pressure rows from TICKET74 with zero congruence-extension failures. It demotes the earlier `base_prefix_consumed` DAG coordinate because exact prefix and consumed lengths make it an unbounded diagnostic rather than a fixed finite state. Eight fixed finite pre-outcome coordinates built from clipped valuation tails, low residues, clipped next valuations, and modular prefix/consumed data are tested instead. None passes observed successor closure, projected-cycle exclusion, and pressure-outcome determinism simultaneously. The coarsest coordinate leaks only `11 / 78,315` sixth-lift rows but retains 66 cyclic nodes and 59 mixed keys. The richest coordinate reduces mixed keys to four but sends `77,998 / 78,315` rows into classes outside the observed source cover. This is a finite compression-versus-state-growth obstruction for the tested grammar, not a Collatz theorem.

Exact result:

```text
fifth open pressure: 15,696
sixth open pressure: 78,315
source identity failures: 0
exact extension failures: 0
fixed finite coordinate families tested: 8
two-layer closure gates passed: 0

coarsest family: 11 novel rows, 66 cyclic nodes, 59 mixed keys
richest family: 77,998 novel rows, 373 cyclic nodes, 4 mixed keys
```

Discarded route:

```text
Treat a bounded DAG rank that contains exact growing lengths as a finite automaton, or choose a coordinate only because it is collision-free at one horizon. A valid induction coordinate must be fixed, successor-closed, outcome-sufficient, and well-founded for every compatible lift.
```

Retained route:

```text
Derive a symbolic successor formula and prove a horizon-independent closure/rank theorem, or construct a nonempty exact compatible pressure tree at every depth and then separately prove that one path represents divergence or a nontrivial cycle.
```

Candidate theorem still missing:

```text
SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath: a fixed pre-outcome coordinate covers every compatible open-pressure successor and carries a strictly decreasing well-founded rank, or there exists an all-depth exact compatible pressure path escaping every certified cover.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
TICKET75 performs no problem-specific coordinate computation for these three problems. Their TICKET75 artifacts transfer only the rule that bounded or horizon-dependent state summaries cannot be promoted without a problem-specific all-height successor theorem.
```

Proof boundary:

```text
TICKET-75 proves or disproves none of the four open problems. It falsifies eight finite Collatz coordinate candidates and identifies a measurable coordinate-design obstruction.
```

### Ticket 76: Exact boundary quotient recurrence

CO-TICKET-76 FourBitBoundaryQuotientRecurrenceAndFixedPrecisionLoss

Artifacts:

```text
data/open-problem/ticket76-symbolic-boundary-recurrence-lab.json
data/open-problem/collatz/co-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/riemann/rh-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/goldbach/gb-ticket-76-symbolic-boundary-recurrence.json
data/open-problem/twin-prime/tp-ticket-76-symbolic-boundary-recurrence.json
```

Status:

```text
symbolic_formula_verified_fixed_precision_closure_refuted_on_tested_precisions_no_global_resolution
```

한국어 요약: TICKET-76은 TICKET75의 압축-상태성장 현상을 exact arithmetic으로 설명한다. modulus `2^b`에서 누적 consumed bits가 `b`에 닿는 valuation은 상위 bit lift에서 바뀔 수 있으므로 먼저 equality step을 rollback하여 lift-stable prefix를 정의한다. 그 prefix의 길이를 `m`, consumed bits를 `s`, `d=b-s`, `A=(3T^m(r)+1)/2^d`, `u=3^(m+1)`라 두면 상위 네 비트 digit `h`를 붙인 자식의 첫 새 valuation은 정확히 `d+v2(A+hu)`다. `v2(A+hu)>4`이면 자식은 같은 prefix에서 미해결이고 다음 quotient는 `(A+hu)/16`이다. fifth/sixth source의 297,104개 자식을 전부 검사한 결과 prefix replay, affine identity, valuation, recurrence failure는 0개였다. 하지만 quotient precision `q=5,9,13,17,21`은 각각 165, 1,536, 1,235, 106, 15개의 reachable successor collision key를 남겼다. 같은 row에서 `q+4`비트를 제공하면 collision은 모두 0개다. 따라서 fixed low-bit repair는 재귀적으로 닫히지 않는다.

English summary: TICKET-76 derives the exact first-boundary recurrence behind the TICKET75 compression-versus-state-growth obstruction. A valuation whose cumulative consumption exactly reaches `b` is not lift-stable, so the audit first rolls that equality step back. For the resulting stable prefix, `T^m(r+h2^b)=T^m(r)+h3^m2^(b-s)`. With `d=b-s`, `A=(3T^m(r)+1)/2^d`, and `u=3^(m+1)`, the first new valuation is `d+v2(A+hu)`. If it remains unresolved after a four-bit lift, then `A_next=(A+hu)/16`. All 297,104 audited children satisfy the replay and recurrence identities with zero failures. Fixed quotient precisions `q=5,9,13,17,21` have 165, 1,536, 1,235, 106, and 15 reachable collision keys, while `q+4` lookahead has zero collisions in every case.

Exact finite and symbolic result:

```text
fifth source rows:  2,873 sources, 45,968 children, 1,398 unresolved-same-prefix
sixth source rows: 15,696 sources, 251,136 children, 7,751 unresolved-same-prefix
combined transition rows: 297,104
prefix/affine/valuation/recurrence failures: 0

fixed-q collision keys:
q=5: 165
q=9: 1,536
q=13: 1,235
q=17: 106
q=21: 15
q+4 lookahead collisions: 0 for every tested q
```

Discarded route:

```text
Append a fixed number of low boundary-quotient bits to the TICKET75 coordinate. On an unresolved lift, division by 16 exposes four new higher bits, and exact reachable witnesses show that the fixed-q successor is not determined.
```

Retained route:

```text
Prove that the reachable boundary quotients occupy a restricted arithmetic subset on which a finite quotient closes, or retain the full 2-adic quotient and find a separate well-founded rank. The counterexample route is an exact all-depth compatible path in this recurrence followed by a separate integer-dynamical proof.
```

Candidate theorem still missing:

```text
ReachableBoundaryRestrictionOrTwoAdicPressurePath: reachable Collatz boundary quotients obey a uniform arithmetic restriction yielding finite successor closure and strict descent, or the exact 2-adic recurrence admits an all-depth compatible pressure path requiring separate divergence/cycle classification.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
No TICKET76 arithmetic or counts are transferred. Only the requirement to account for information lost under each problem's exact scale/refinement recurrence is transferred.
```

Proof boundary:

```text
TICKET-76 proves the displayed recurrence identity and bounded collision statements. It does not prove Collatz, produce a divergent integer orbit, or solve any of the other three problems.
```

### Ticket 77: Fixed stable-prefix boundary orbit classification

CO-TICKET-77 FixedStablePrefixBoundaryOrbitAndTwoAdicGhostClassification

Artifacts:

```text
data/open-problem/ticket77-fixed-prefix-boundary-orbit-lab.json
data/open-problem/collatz/co-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/riemann/rh-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/goldbach/gb-ticket-77-fixed-prefix-boundary-orbit.json
data/open-problem/twin-prime/tp-ticket-77-fixed-prefix-boundary-orbit.json
```

Status:

```text
fixed_prefix_boundary_orbit_classified_no_collatz_resolution
```

한국어 요약: TICKET-77은 TICKET76의 경계 몫 재귀식을 고정 stable prefix 전체에서 분류한다. `u=3^(m+1)`이고 `h(A)`가 `A+h(A)u = 0 mod 16`을 만족하는 유일한 4비트 digit일 때 `P(A)=(A+h(A)u)/16`이다. Reachability에서 `3∤A`이고 `A>u`이면 `P(A)<A`다. `A<u`에서는 `16^(-1)A mod u`의 최소 양의 대표이며 LTE로 주기가 정확히 `3^m`임을 얻는다. 첫 초안은 홀수 `P(A)`를 stable-prefix extinction으로 잘못 승격했다. 실제로 홀수는 valuation이 현재 modulus 경계에 정확히 닿는 equality 사건이며, TICKET76 규칙에 따라 rollback된다. 따라서 strict pressure 구간만 끝나고 정규화된 fixed-prefix 궤도는 계속된다. all-depth compatible cylinder는 `T^m(N)=-1/3`인 2-adic ghost로 수렴하며 양의 정수가 아니다.

English summary: TICKET-77 classifies the TICKET76 recurrence for a fixed stable prefix. The map contracts while `A>u` and then becomes the inverse-16 orbit modulo `u=3^(m+1)`, with exact period `3^m`. Odd successors end only strict-beyond-boundary runs; the equality valuation is rolled back and the normalized orbit continues. Its compatible limit is a 2-adic preimage of `-1/3`, not a positive integer.

Exact audit:

```text
reconstructed fifth/sixth boundary sources: 18,569
strict segments reaching equality:          18,569
maximum strict-pressure steps:               15
prerequisite failures:                       0
one-step identity failures:                  0
unexpected strict cycles:                    0
trace-guard failures:                        0
finite orbit audit:                          m=0,...,10, failures 0
```

Discarded route:

```text
Treat odd P(A) as extinction of the stable prefix. It is an equality-boundary event whose valuation must be rolled back before the next lift.
```

Closed counterexample route:

```text
Promote a fixed-prefix all-depth compatible cylinder directly to a natural-number counterexample. Its exact completion is a 2-adic preimage of -1/3, not a positive integer.
```

Candidate theorem still missing:

```text
ChangingPrefixNaturalAdmissibilityRank: every positive-integer boundary refinement enters the known basin or strictly decreases a global rank, while every nondecreasing compatible limit is proved non-natural.
```

Transfer discipline for RH, Goldbach, and Twin Prime:

```text
No TICKET77 Collatz orbit theorem or count is transferred. The other artifacts record only the discipline of classifying normalized recurrent states and testing whether completion points are admissible for the original problem.
```

Proof boundary:

```text
TICKET-77 classifies fixed-prefix compatible completions as 2-adic ghosts. It does not exclude infinitely many changing-prefix events, divergence, or nontrivial accelerated cycles, and it proves or disproves none of the other three open problems.
```

### Ticket 78: Finite-cylinder natural-admissibility no-go

CO-TICKET-78 FiniteValuationCylinderNaturalDensityNoGo

Artifacts:

```text
data/open-problem/ticket78-finite-cylinder-admissibility-no-go-lab.json
data/open-problem/collatz/co-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/riemann/rh-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/goldbach/gb-ticket-78-finite-cylinder-admissibility-no-go.json
data/open-problem/twin-prime/tp-ticket-78-finite-cylinder-admissibility-no-go.json
```

Status:

```text
finite_two_adic_natural_separator_refuted_exactly_no_collatz_resolution
```

한국어 요약: positive accelerated valuation word `a=(a_1,...,a_m)`와 `S=sum a_i`에 대해 affine composition은 `T^m(n)=(3^m n+C_m)/2^S`다. terminal odd 조건은 유일한 cylinder `n=r_a mod 2^(S+1)`를 주고, 이 cylinder에는 `r_a+q2^(S+1)` 꼴의 양의 정수가 무한히 많다. 따라서 fixed residue bits, finite valuation/parity word, continuous finite-state 2-adic classifier는 TICKET77 ghost의 비자연성을 인증할 수 없다. 모든 유한 2-adic neighborhood에 자연수가 있기 때문이다.

English summary: Every finite accelerated valuation word defines one exact residue class modulo `2^(S+1)`, and that class contains infinitely many positive integers. Positive integers are dense in `Z_2`, so no locally constant finite-prefix classifier can accept every positive integer and reject a TICKET77 ghost.

Exact audit:

```text
total valuation S:                 1,...,16
finite valuation words:           65,535
expected composition count:       65,535
positive representatives replayed: 262,140
residue collisions:               0
formula failures:                 0
representative replay failures:   0
count-identity failures:           0
```

Literature boundary:

```text
The 2-adic shift conjugacy is established by Bernstein and Lagarias. TICKET78 claims no rediscovery. Its project-specific role is to connect finite accelerated valuation cylinders to the corrected TICKET77 boundary state and enforce a no-go guard.
```

Discarded route:

```text
Any natural-admissibility classifier or rank that factors through fixed residue bits, a finite parity/valuation word, or another continuous finite-state coordinate on Z_2.
```

Candidate theorem still missing:

```text
ArchimedeanTwoAdicCoupledDescent: every positive-integer accelerated trajectory enters the known basin or strictly decreases a well-founded rank using both Archimedean height and growing 2-adic precision; the rank cannot factor through a fixed finite 2-adic quotient.
```

Transfer discipline:

```text
No Collatz formula, count, density theorem, or conclusion is transferred to RH, Goldbach, or Twin Prime. Their artifacts record only a requirement to prove a problem-specific local-to-global obstruction before using the analogy.
```

Proof boundary:

```text
TICKET-78 proves a proof-route no-go lemma. It does not construct the required coupled rank, prove Collatz, or solve any of the other three problems.
```
## TICKET79: bounded Archimedean-two-adic one-step rank no-go

TICKET79 attacks the first rank class left open by TICKET78:

```text
R(n)=alpha*log(n)+b(s(n))
```

For a finite state set and bounded correction, all coefficient signs fail. The exact expansion family `2^(m+1)q-1` gives arbitrarily long valuation-1 blocks; the exact nonterminal contraction family `(5*2^(2r+1)-1)/3` maps to 5; and the zero-log finite-state case fails by pigeonhole repetition. This is a theorem about the proposed rank family, not about Collatz itself.

The next accepted route is a minimal-counterexample contrapositive. Assuming a least counterexample `N`, every valuation prefix must obey

```text
2^S*N <= 3^m*N+C_m.
```

TICKET80 must combine these inequalities with exact cylinder congruences. A finite-horizon fit, bounded residue table, or an unbounded correction without a proved lower bound is not an acceptable proof object.
## TICKET80: least-counterexample finite-prefix compactness no-go

TICKET80 attacks the direct contrapositive proposed after TICKET79. A least counterexample must satisfy `A^j(N)>=N` for every prefix, but every finite subset of those inequalities remains satisfiable above every finite lower bound:

```text
n=2^(H+1)*ceil((B+1)/2^(H+1))-1
A^j(n)=3^j*2^(H+1-j)*q-1>n for 1<=j<=H.
```

The nested `q=1` witnesses escape to infinity in ordinary size while converging to `-1` in `Z_2`. Thus finite satisfiability and 2-adic compactness do not produce a positive counterexample or a contradiction. A positive ordinary limit requires eventual stabilization of the least nonnegative cylinder residues.

The next accepted route must track one fixed stabilized integer and derive a horizon-independent upper bound. Repeating a finite-prefix search at a larger bound is no longer an admissible proof strategy.

## TICKET81: Mersenne first-compensation no-go

TICKET81 tests the first positive-integer stabilization repair suggested by TICKET80. Let `N_k=2^k-1`. The first `k-1` accelerated steps have valuation one and satisfy

```text
A^j(N_k)=3^j*2^(k-j)-1>N_k, 1<=j<=k-1.
```

The exact cylinder modulus at that depth is `2^k=N_k+1`, so its least residue is already the positive integer `N_k`. Nevertheless,

```text
A^k(N_k)=oddpart(3^k-1)
a_k=2 for odd k
a_k=3+v2(k) for even k.
```

The first compensation step descends exactly for `k in {2,4,8}`. It does not descend for every odd `k>=3`, for `k=6`, or for any even `k>=10`. The latter infinite class follows from `2^(2+v2(k))<=4k` and `(3^k-1)/(4k)>2^k-1`.

Rejected candidate theorem:

```text
The first non-1 valuation after any sufficiently long stabilized expansion block forces descent.
```

Accepted next target:

```text
MersenneAdaptiveCompensationWindow: prove an explicit cumulative valuation window L(k) sends every Mersenne start below itself.
```

Even if established, this target is an infinite-family theorem only. Extending it from Mersenne starts to every stabilized positive cylinder without a separate argument would reintroduce the full Collatz conjecture.

## TICKET82: fixed Mersenne compensation-window no-go

TICKET82 refutes every constant-window repair of TICKET81. For the reference exponent `k=3`, the first post-compensation value is 13 and its additional valuation word is `3,4,2,2,...`. The symbolic family

```text
x_t(k)=A^(k+t)(2^k-1)=(3^(k+t)+c_t)/2^d_t
c_(t+1)=3*c_t+2^d_t
```

is preserved through any fixed horizon `H` by the explicit progression `k=3 mod 2^(2H+3)` for `H>=2`. Since each fixed symbolic iterate grows like `3^k` divided by a constant while the start grows like `2^k`, every sufficiently large exponent in that progression remains above its start through the whole window.

Therefore Mersenne post-expansion stopping delay is unbounded. The route “choose a large but constant lookahead” is permanently rejected. The next admissible target is

```text
MersenneGrowingWindowDescent: construct an explicit unbounded L(k) and prove some post-expansion iterate through L(k) lies below 2^k-1.
```

This does not imply divergence; each constructed finite prefix may descend later. It also does not transfer a Collatz theorem to the other three problems.

## TICKET83: Mersenne half-log delay lower bound

For `k_H=3+2^(2H+3)`, the TICKET82 symbolic family satisfies `|c_t|<2^d_t` and `d_t<=2H+4`. Since `k_H>=4H+11`, exact integer inequalities give every post-expansion iterate through `H` above its start. As `k_H<2^(2H+4)`,

```text
D(k_H)>H>(1/2)*log2(k_H)-2.
```

This rejects every universal `o(log k)` Mersenne window and every logarithmic coefficient below `1/2`. The coefficient is certified, not claimed optimal. The next target is `MersenneLogWindowDichotomy`: optimize the lower coefficient and seek or refute a finite logarithmic upper coefficient for all Mersenne exponents.

## TICKET84: accessible 2-adic cycle and two-thirds log bound

The odd 2-adic equation `3^kappa=-13` produces the post-value cycle `-7 -> -5 -> -7` with valuation word `2,1`. Unique finite exponent residues modulo `2^(d_H-1)` preserve this word through `H`; adding one period produces positive ordinary exponents. The ghost is never classified as natural. Exact affine and growth bounds give

```text
D(k_H)>H>(2/3)*log2(k_H)-1.
```

Thus every coefficient below `2/3` fails infinitely often. The next target classifies all periodic valuation words whose cycles lie in the 2-adic exponent image and optimizes reciprocal mean valuation.

## TICKET85: accessible cycle coefficient supremum

The exact family `w_m=(2,1^(m-1))` has cycle value `C_m/(2^(m+1)-3^m)`, is `1 mod 8`, and has reciprocal mean `m/(m+1)`. Therefore the accessible coefficient supremum is 1. It is not attained because the all-ones fixed point `-1` targets `7 mod 8`, outside the odd exponent image. Choosing `m=H` gives

```text
D(k_H)>H>log2(k_H)-2.
```

All subunit logarithmic coefficients, even with arbitrary fixed additive constants, are rejected. The next target is the coefficient-one additive boundary and a separate universal Mersenne upper bound.

## TICKET86: infinite coefficient-one Mersenne delay

The cycle target at horizon `H` reduces exactly to the fixed congruence

```text
3^(r_H+1) = -7 mod 2^(H+3).
```

The least odd residues are nested: the next lift either keeps `r_H` or adds the new top bit. Top-bit additions occur infinitely often, because eventual stabilization at a positive ordinary integer `r` would make `3^(r+1)+7` divisible by arbitrarily high powers of two and hence force the impossible equality `3^(r+1)=-7`.

At every top-bit height, `2^H<=r_H<2^(H+1)`. The exact valuation prefix, affine constant bound, and elementary growth estimate prove

```text
D(r_H)>H,
D(r_H)>=H+1>log2(r_H).
```

This refutes `D(k)<=log2(k)` on an infinite Mersenne-exponent subsequence. It does not refute `D(k)<=log2(k)+C` for a positive constant, does not construct a divergent orbit, and does not resolve Collatz. The next target is `TwoAdicDigitRunBoundary`: connect binary zero-run structure of the fixed 2-adic logarithm to an unbounded additive delay excess, or produce a rigorous obstruction.

## TICKET87: two-adic digit runs and additive-one delay

The fixed exponent solving `3^(r+1)=-7` has infinitely many one bits and infinitely many zero bits. Finitely many one bits would stabilize the nested residues at a nonnegative integer. Finitely many zero bits would make the exponent an eventually-all-one negative integer. Either case turns the 2-adic equation into an impossible rational equality.

Consequently one-to-zero transitions occur infinitely often. At each transition the same positive exponent preserves the exact valuation prefix for one additional horizon. Reusing the affine growth bound and integrality of the delay gives

```text
D(k)>log2(k)+1
```

for infinitely many positive odd exponents. A zero run of length `L` gives the more general finite bound `D(k)-log2(k)>min(L,k-H-2)`. The 262,144-height audit observes a length-16 run and certifies one finite excess above 16, but this does not prove unbounded run length. The next target is infinitude of the `100` pattern, which would cross additive constant 2 on an infinite subsequence.

## TICKET88: run-length-two promotion no-go

Two-sided digit infinitude does not imply `100` recurrence. The explicit digit sequence with zeros at square positions is non-eventually-periodic, has infinitely many zeros and ones, and has no adjacent zeros. The natural dual exponent `s=-r` complements every bit above bit zero, but its post-value `-5/7` enters the exact accelerated cycle `5/7 -> 11/7 -> 5/7` with valuation word `(1,3)`. Its reciprocal mean is `1/2`, so the coefficient-one delay geometry is not preserved.

TICKET88 therefore rejects both the generic symbolic inference and the complement transfer. The next theorem must use the arithmetic identity of the specific fixed logarithm:

```text
FixedLogGoldenMeanExclusion:
for every H0, some h>=H0 has r_h r_(h+1) r_(h+2)=100.
```

The 32,753 finite observed runs of length at least two are falsification evidence only.

## TICKET89: fixed-log golden-mean valuation reduction

For consecutive top-bit heights `H<J` and the positive least residue `k=r_H`, exact lift failure at `J` gives

```text
v2(3^(k+1)+7)=J+2,
v2(3^(k+1)+7)-floor(log2(k))=(J-H-1)+3.
```

Therefore `100` at `H` is equivalent to valuation excess at least five. Eventual golden-mean membership is equivalent to an eventual excess cap of four. The no-`00` subshift contains uncountably many transcendental 2-adic numbers and has positive entropy, so transcendence and counting alone cannot contradict the cap. The next theorem is `FixedLogValuationExcessFiveInfinitude` for the exact nested residues.

## TICKET90: normalized-error ghost-lasso no-go

Define `e_H=(3^(r_H+1)+7)/2^(H+3)`. Its parity is the next lift bit, and its exact branch recurrence is forced by `A_H=(3^(2^(H+1))-1)/2^(H+3)`. The identity `A_(H+1)=A_H+2^(H+2)A_H^2` yields the limiting odd forcing constant `beta=-7 log_2adic(-3)/4`. The limiting map fixes `e=beta`, so every fixed precision contains a target-avoiding lasso. Any continuation must use precision growing with H and quantitatively separate the actual error orbit from this ghost.

## TICKET91: error-tail conjugacy and invariant-set correction

Let `R` be the fixed 2-adic solution of `3^(R+1)=-7` and write `R=r_H+2^(H+1)t_H`. Substitution gives

```text
e_H = 7(1-(1+2^(H+3)A_H)^(-t_H))/2^(H+3),
e_H = 7A_H t_H (mod 2^(H+3)),
e_H = gamma t_H (mod 2^(H+2)),
gamma = 7 log_2adic(-3)/4.
```

The tail update is the one-sided binary shift. Multiplication by odd `gamma` conjugates it to the limiting normalized-error map. Hence `beta=-gamma` corresponds exactly to `t=-1`, the all-one tail. Distance from beta measures only the number of initial future one bits, so beta separation cannot force `00`.

The complete target-avoiding set is the golden-mean subshift `G` of tails without `00`; its error-coordinate image `gamma G` is invariant and has `F_(n+2)` words at depth `n`. TICKET91 therefore retires `GrowingPrecisionErrorGhostSeparation` as insufficient and replaces it with `GoldenMeanInvariantSetEscape`. No `00` recurrence, additive-two infinite delay result, or Collatz theorem is claimed.

## TICKET92: scale-sensitive threshold correction

For Collatz, consecutive top-bit heights `H<J` give

```text
Delta_H = v2(R-r_H)-floor(log2(r_H)) = J-H.
```

The `100` target is exactly `Delta_H>=3`. Dividing by `H` produces `1+Delta_H/H`, which converges to one for every bounded defect and therefore cannot distinguish the target from an eventual no-`00` sequence. The next admissible target is `FixedLogSecondOrderDefectRecurrence`; first-order irrationality exponents and upper-bound linear-form estimates are retired for this constant-additive event.

For Twin Prime, the former TP-TICKET-14 threshold `M_k>2/k` was not Maynard's criterion. Proposition 4.2 uses `ceil(theta*M_k/2)`. With unconditional `theta<1/2`, a two-prime conclusion requires a certified strict `M_k>4` in the limiting threshold. The 17 legacy scores were not variational certificates, so all implied bounded gaps were removed. A valid bounded-gap certificate would still not isolate exact gap 2; the remaining target is a parity-breaking exact-pair correlation lower bound.

## TICKET93: exact twin-correlation excess bridge

Set `C_2(x)=sum Lambda(n)Lambda(n+2)`. Proper prime powers contribute at most

```text
B(x)=2 sqrt(x+2) floor(log2(x+2)) log^2(x+2).
```

Thus unbounded `C_2(x)-B(x)` forces the genuine twin-prime weight to be unbounded and proves twin-prime infinitude. The bridge is exact and unconditional, but the required lower bound remains open.

The truncated divisor surrogate `Lambda_R=sum_{d|n,d<=R}mu(d)log(R/d)` is not a minorant. For every tested truncation it exceeds `Lambda` pointwise at many integers and creates positive shift-two pairs with exact product zero. Its positive correlation cannot be promoted without a signed Type II remainder estimate. The next theorem is `ShiftTwoTypeIICorrelationExcess`.

## TICKET94: signed remainder and Goldbach bridge

For Twin Prime, write `Lambda=alpha Lambda_R+E_R` and expand the shift-two correlation exactly. The surrogate main term is corrected by two cross terms and one residual autocorrelation. Separate Cauchy bounds are negative for every tested truncation, so L2 proximity alone cannot supply the one-sided lower bound. The next theorem must estimate the combined signed remainder directly.

For even `N`, the Goldbach correlation `G(N)=sum Lambda(n)Lambda(N-n)` has proper-prime-power contamination at most `2 sqrt(N) floor(log2(N)) log^2(N)`. Correlation above this threshold certifies a genuine prime representation. Binary Goldbach is reduced to a uniform all-large-even correlation excess plus finite verification; neither part is claimed complete.

## TICKET95: sharp contamination and equivalence audit

Define the cumulative proper-prime-power Mangoldt mass

```text
H(y)=sum_{m<=y, m=p^k, k>=2} Lambda(m).
```

Charging a contaminated pair to its proper-power endpoint proves the sharper unconditional bounds

```text
Twin:    E_pp(x) <= log(x+2)(H(x)+H(x+2)),
Goldbach: E_pp(N) <= 2 log(N) H(N).
```

These replace the TICKET93/94 exponent-count envelopes. Every stored checkpoint passes the new bounds, and their numerical size is roughly 27 to 238 times smaller. A Goldbach FFT screen over all 499,999 even targets through one million observes a positive sharp margin for every even `N>=40`; the ten smaller nonpositive criterion cases all have direct prime witnesses. The screen is explicitly labelled non-rigorous floating-point evidence.

TICKET95 also audits the Twin signed-remainder target:

```text
D_R=C_2-alpha_R^2S_R,
D_R>=-alpha_R^2S_R+B_#+omega  iff  C_2>=B_#+omega.
```

Thus the TICKET94 target is a valid reformulation but not a weaker theorem. It remains useful only if an independent Type II estimate controls `D_R` without importing the exact correlation. The retained targets are `IndependentShiftTwoCorrelationExcess` and `UniformBinaryMinorArcDominance`. No open conjecture or counterexample is claimed.

## TICKET96: Fourier phase-information audit

Let `F(z)=sum Lambda(n)z^n` and zero-pad beyond twice the audited range. Exact inverse DFT coefficient extraction gives

```text
Goldbach: coefficient_N F(z)^2 = G(N),
Twin:     coefficient_shift2 |F(z)|^2 = C_2(x).
```

Every frequency mask therefore supplies an exact signed major/minor decomposition. Replacing the signed minor coefficient by its Parseval-energy envelope is valid but loses decisive information. At 10,000 and 100,000, 36 low-denominator mask configurations per scale are replayed; no mask with density at most ten percent certifies either TICKET95 contamination budget through energy alone.

Two abstract countermodels explain the failure. Goldbach minor magnitudes admit conjugate-symmetric phase choices that align the target coefficient negatively. Twin total minor energy admits conjugate-symmetric placement at frequencies with negative shift-two cosine. These countermodels are not prime sequences; they prove only that phase-blind premises are logically insufficient without extra arithmetic constraints.

The retained targets are

```text
ArithmeticMinorArcPhaseCancellation,
ShiftTwoSpectralLocalizationOrTypeIICancellation.
```

Dense data-dependent masks and exact sampled DFT replay are not promoted to asymptotic theorems. No open conjecture or certified prime counterexample is claimed.

## TICKET97: optimal periodic projection and residual-sign audit

For each fixed modulus `W`, project Lambda onto its exact finite-interval residue-class means. This conditional expectation is the unique L2-optimal W-periodic model, and its residual has zero mean in every residue class. Goldbach and shift-two correlations split exactly into periodic main, two cross terms, and a residual correlation.

The audit uses `W=2,6,30,210,2310` at scales 10,000 and 100,000. All projection and reconstruction contracts pass, but no separate norm-only lower bound certifies either TICKET95 sharp budget. Fixed-modulus one-point arithmetic structure remains insufficient.

The explicit signed residual

```text
[1,1,-1,-1,-1,-1,1,1]
```

has zero sums in both mod-2 residue classes while producing additive coefficient `-4` and shift-two coefficient `-2`. This proves an information no-go for residue means, not a prime counterexample.

The retained targets are `GrowingModulusBinaryResidualCancellation` and `GrowingModulusShiftTwoResidualCancellation`: the modulus must grow under independent distribution estimates, and the signed residual correlation must be controlled by Type II or higher-order uniformity.

## TICKET98: growing-modulus leakage boundary

For a finite dataset indexed by `0,...,L-1`, a fitted residue projection with `W>=L` is the identity: distinct indices have distinct residues, every occupied residue mean equals its only observation, and therefore `P_W x=x`, `E_W=0`. Any norm certificate at that point is an exact replay of the observed target correlation.

The primorial audit through `W=9,699,690` uses scales 10,000, 100,000, and 1,000,000. At each scale the first Goldbach and Twin certificate is exactly the first row-unique modulus; there are no non-row-unique certificates. Even the near-saturated case `N=1,000,000`, `W=510,510`, with at most two observations per occupied residue, certifies neither target.

The fitted-growing-modulus shortcut is retired. The retained targets are `OutOfSampleGrowingModulusBinaryResidualCancellation` and `OutOfSampleGrowingModulusShiftTwoResidualCancellation`: estimate the arithmetic projection independently of the evaluated correlation, retain a nondegenerate occupancy regime, and prove a signed residual estimate uniform in scale. This leakage theorem proves none of the four conjectures.

## TICKET99: out-of-sample and external local model

The period-parity cross-fit uses disjoint Lambda samples for training and evaluation and rejects empty evaluation sets. Across 120 preregistered configurations, separate norm lower bounds certify neither Goldbach nor Twin Prime.

The external coprime model `A_W(n)=W/phi(W) 1_(n,W)=1` removes fitted-data dependence entirely. CRT gives the exact common lower density

```text
d_W = 2 product_{3<=p|W}(1-1/(p-1)^2),
M_G(N), M_2(x) >= d_W max(0,scale+1-W).
```

Thus the main term is linear and target-independent. The only unresolved object is the signed residual. For the largest primorial `W(n)` with `W(n)^2<=n`, the finite candidate

```text
R_W(n) >= -1.6 M_W(n)/log(n)
```

has zero post-calibration failures through one million on both tracks. If proved uniformly and independently, it combines with the `o(n)` prime-power contamination budgets to imply Goldbach after finite verification and Twin Prime infinitude. The screen is double-precision candidate discovery, not proof. Generic W-trick transference and one-point progression control do not resolve these affine-degenerate binary residuals.

## TICKET100: extended residual and joint Vaughan cancellation

The `K=1.6` candidate has zero finite failures through every even Goldbach target at 6M and every cumulative Twin target at 10M, including the first `210 -> 2310` primorial transition. This remains finite evidence.

With `Lambda=I_(U,V)+II_(U,V)`, substitute one factor only:

```text
C-M = (<I,Lambda_shift>-M) + <II,Lambda_shift>.
```

At Goldbach `N=930,930`, the Type II component alone has required constant `K=7.9099`, whereas the joint residual's worst constant remains below `1.6`. This is a concrete counterexample to separate componentwise K/log lower bounds. The structured term and Type II term must be estimated jointly with their signs intact.

The contrapositive program is now exact: a large Goldbach counterexample or finite Twin set forces the residual-to-main ratio toward `-1`, contradicting any independently proved joint `-K/log n` lower envelope. The remaining targets are `JointVaughanGoldbachResidualEnvelope` and `JointVaughanShiftTwoResidualEnvelope`.

## TICKET101: balanced cutoff frontier and energy-equivalence audit

The TICKET100 `U=V=100` obstruction is not promoted without a parameter audit. At scale one million, TICKET101 evaluates 39 Vaughan cutoff pairs, including 28 balanced pairs satisfying `U,V<=N^(1/3)=100`.

Goldbach has no separated-budget survivor in that balanced range. The best tested row remains `U=V=100`, with structured constant `1.5791`, Type II constant `7.9099`, and total `9.4890`. A numerical pass first appears at `U=V=960`, but only 314 Type II coordinates remain. At `U=V=1000`, Type II is zero and the structured term equals Lambda. This is decomposition collapse, so the retained Goldbach target is `JointBalancedVaughanGoldbachResidualEnvelope`.

Twin Prime has four balanced survivors. The best tested pair `U=100,V=84` has a nonzero Type II support of 244,204 coordinates and constants

```text
structured K = 1.3889576,
Type II K    = 0.1710919,
sum          = 1.5600495 < 1.6.
```

This corrects the broad joint-only continuation. The next Twin target is `SeparatedBalancedVaughanTwinBudgets`, with rounded discovery budgets `1.40` and `0.18`. Both all-scale inequalities remain unproved.

Finally, the Goldbach reflection identity and Twin shift-mismatch identity rewrite correlation as an energy deficit. The rewrite is exact, but the desired energy inequality is algebraically equivalent to the original correlation lower bound. It is not a reduction unless an independent mismatch theorem contributes new information. TICKET101 proves neither a conjecture nor a conjecture counterexample.

## TICKET102: Twin dyadic holdout and finite-constant correction

Use the data-independent scale-local rule `U(X)=round(X^(1/3))`, `V(X)=round(0.84U(X))` and inspect every `x` in `(X/2,X]`. The registered structured budget `K_S=1.40` is refuted at `X=2M`: all one million post-selection points fail, with maximum required constant `1.9532`. The Type II `K_II=0.18` budget has no failures. This is a proof-strategy counterexample, not a Twin Prime counterexample.

The former `1.6` gate was unnecessarily strong. For any fixed finite `K_S,K_II`, the two component bounds imply

```text
C_2(x) >= M(x)(1-(K_S+K_II)/log(x)).
```

The external local main has a positive linear lower bound up to lower-order modulus loss, and proper-prime-power contamination is `o(x)`. Thus any horizon-uniform finite constants are sufficient; no optimization against `1.6` is needed.

After the failure is observed through 4M, register `K_S=4,K_II=1` before opening the 8M block. All four million fresh points pass. The maximum required structured constant is `3.3068`, Type II is nonnegative throughout the block, and Type II support is `24.31%`. Support is only a noncollapse guard, not an analytic Type II estimate.

The retained target is `UniformFiniteDyadicSeparatedVaughanTwinBudgets`. RH returns to non-circular kernel positivity, Collatz to `GoldenMeanInvariantSetEscape`, and Goldbach to joint balanced signed cancellation. TICKET102 proves none of the four conjectures.

## TICKET103: exact Twin local-block audit

TICKET102's endpoint audit uses cumulative component correlations from zero. TICKET103 fixes one external model and one Vaughan split per dyadic horizon, then evaluates the exact identity only on `(X/2,X]`. This removes the possibility that earlier positive Type II mass hides a negative current block.

The seven principal blocks from 125K through 8M have positive Type II sums. Their maximum structured required constant is `3.7617`, maximum Type II required constant is `0`, and maximum joint required constant is `0.6430`. All reconstruction and support contracts pass.

Universal positivity is nevertheless false. At `X=1000`, the local Type II correlation on `(500,1000]` equals `-174.7165`, requiring `K_II=1.7515`. This exact finite counterexample retires Type II nonnegativity as an identity or all-scale lemma. It does not refute eventual finite bounds and is not a Twin Prime counterexample.

The retained target is `UniformDyadicLocalVaughanTwinBlockBudgets`: prove some fixed finite local structured and Type II constants on every sufficiently large dyadic block. Such bounds, combined with the linear local main and `o(X)` contamination, are sufficient for twin-prime infinitude. TICKET103 proves none of the four conjectures.

## TICKET104: exact Type II weighted-Möbius anatomy

Expanding the local Vaughan Type II kernel gives the exact finite identity

```text
T_X = sum_{d>U} mu(d) A_X(d),
A_X(d) >= 0.
```

The weights contain `Lambda(r)Lambda(drm+2)` on the current dyadic block. Thus the open estimate is weighted Möbius cancellation against shifted-prime mass, not an unweighted Mertens bound.

The identity and Abel summation replay to numerical errors below `1e-9`. At 125K, 1M, and 2M the actual Type II term is positive. Independent negative-term bounds require constants `21.75,34.79,39.92`; Abel summation followed by triangle inequality requires `354.06,799.04,1088.15`. At `X=1000`, actual required `K=1.7515` while the Abel-triangle envelope requires `61.83`.

This does not prove those envelopes diverge. It refutes presenting their finite information-losing forms as the desired cancellation estimate. The retained theorem is `WeightedMobiusShiftedPrimeDyadicCancellation`, preserving the relation between Möbius signs and weight differences before taking absolute values. TICKET104 proves none of the four conjectures.

## TICKET105: coprime progression centering

For each `q=dr`, replace the shifted prime value by its independent progression mean `q/phi(q)` when `q` is odd and zero when `q` is even. This produces an exact baseline-plus-centered decomposition of the TICKET104 weighted Möbius sum.

The identity replays below `1.7e-10` through 2M. At 125K, 1M, and 2M, negative centered-mass bounds require `K=4.50,5.15,5.41`, compared with the uncentered `21.75,34.79,39.92`. Full-vector Cauchy-Schwarz remains much weaker at `26.69,37.12,41.15`.

The remaining term couples `mu(d)` to arithmetic-progression errors `Lambda(drm+2)-dr/phi(dr)`. This is the precise object for dispersion or bilinear large-sieve analysis. The retained target is `MobiusWeightedPrimeProgressionDiscrepancyBound`. Finite improvement after centering is not a proof of a uniform bound, and TICKET105 proves none of the four conjectures.

## TICKET106: modulus grouping and sparse-progression leakage

Combine every repeated factorization `q=dr` before taking norms. The exact centered sum becomes `sum_q c_X(q)Delta_X(q)` and replays below `4.3e-10`. At 2M, however, grouped Cauchy needs `K=249.12` versus outer-`d` `41.15`, and grouped negative mass needs `55.29` versus `5.41`.

Occupancy explains the failure. Moduli with at most one block sample form `72.31%` of support and supply `64,933.8` of centered total `67,608.8`. Their progression cells identify individual rows, analogous to TICKET98's row-unique fitted-modulus leakage. Positive sparse-tail mass is not a dense distribution theorem.

The retained target is `NonSparseModulusTwinDispersionWithSparseTailControl`: separate a nondegenerate-occupancy dispersion estimate from an independently controlled sparse tail. TICKET106 proves none of the four conjectures.

## TICKET-107: sparse-tail Vaughan recombination

TICKET107 maps every occupancy-one modulus `q` back to its unique integer `n=qm`, combines repeated n values, and compares the resulting q-built Type II vector with an independently constructed Vaughan decomposition. All q-to-n, Vaughan-vector, and correlation identities pass through 8M.

At 8M, 1,589,098 sparse q cells compress to 1,099,268 n cells; 247,461 n cells receive two sparse-q representations, and n-grouping retains only `69.53%` of q-level L1 mass. The structured residual is `-1,281,289.5`, sparse Type II is `+399,460.6`, dense Type II is `+756,121.9`, and the full residual is `-125,707.0`. The structured-plus-sparse required constant is `2.59`, versus `0.37` for the full joint residual.

This refutes fixed-sign sparse-tail and independent one-sided component-budget shortcuts on the audited data. The retained theorem is `JointStructuredSparseDenseTwinDispersion`, which must preserve all three signed components through the final uniform estimate. TICKET107 proves none of the four conjectures.

## TICKET-108: joint equivalence no-go and smoothed excess bridge

TICKET108 recombines `Lambda=I+II_sparse+II_dense` symbolically and numerically. The proposed joint hard-cutoff lower bound is exactly the original correlation residual lower bound; the maximum audited equality error through 8M is below `4.2e-9`. `JointStructuredSparseDenseTwinDispersion` is therefore discarded as a no-reduction restatement.

The replacement fixes the nonnegative bump `W(t)=16(t-1/2)(1-t)` on `[1/2,1]`. Since `0<=W<=1`, the weighted proper-prime-power contamination is at most the explicit TICKET93 bound `B(X)`. Thus `limsup(S_W(X)-B(X))=+infinity` implies infinitely many twin primes by contrapositive.

The bump improves only 2/6 finite blocks and worsens all four from 1M through 8M, so it is retained for Fourier/Mellin transform structure rather than numerical dominance. The next target is `SmoothedShiftTwoTypeIICorrelationExcess`. TICKET108 proves none of the four conjectures.

## TICKET-109: spectral phase audit

TICKET109 proves the exact finite identity `sum f(n)f(n+2)=N^(-1)sum |F(k)|^2 cos(4 pi k/N)` for the symmetric fixed bump, with maximum error below `2.4e-10` through `X=1,048,576`. The identity is equivalent to the correlation and is not counted as a lower-bound theorem.

Every tested one-band origin-centered low-frequency lower bound is negative. At the largest horizon the positive phase contribution is `1.829M`, the negative contribution is `-1.370M`, the exact correlation is `0.459M`, and the best tested sufficient lower bound is `-3.338M`.

The discarded route is single-origin frequency concentration with worst-case outside phase. The retained target is `RamanujanMajorArcPhaseMarginWithMinorArcControl`, combining rational major arcs and an independently controlled Type II minor-arc remainder. TICKET109 proves none of the four conjectures.

## TICKET-110: rational major-arc budget

TICKET110 fixes all reduced rational centers `a/q`, `q<=Q`, and widths `Q/(qX)` before reading target contributions, then partitions the discrete spectrum exactly. At `X=1,048,576`, `Q=32` produces major contribution `461,203.6`, actual minor contribution `-2,063.7`, and exact correlation `459,139.9`.

The trivial minor-energy lower bound is `-3,105,699.1`, yielding total lower bound `-2,644,495.5`. Thus rational masking captures the observed arithmetic signal but cannot replace a signed Type II minor-arc estimate.

The retained target is `FixedBumpMajorArcAsymptoticWithTypeIIMinorPowerSaving`. TICKET110 proves none of the four conjectures.

## TICKET-111: Vaughan Type II minor cross-spectrum

TICKET111 connects the fixed `Q=32` rational arc mask to the exact Vaughan decomposition. For the symmetric bump sequence, the shift-two correlation and its fixed minor part split exactly into Type I and Type II cross-spectra against the shifted full von Mangoldt target. Component reconstruction errors remain below the registered tolerance through the fresh 2M holdout.

Consider every proof template that partitions the fixed minor bins, applies Cauchy-Schwarz independently on each cell, and discards complex phase. Its envelope is bounded below by the singleton-bin expression

```text
E_bin(X)=sum_minor m_k |TypeII_hat(k)||Lambda_hat(k)|/N.
```

This smallest phase-blind envelope fails on all five audited horizons. At 2M, known major plus Type-I minor is `929,258.9`, `E_bin=7,596,484.2`, and the resulting lower bound is `-6,667,225.4`. This is a finite no-go for the stated argument class, not for Type II analysis itself.

The candidate `TypeII_minor >= -X^(-1/6)E_bin` was frozen after the rows at or below 1M. It survives the first post-selection 2M holdout: actual Type-II minor `+14,783.4`, candidate envelope `671,440.7`, and finite lower expression `257,818.2`. Finite survival does not prove uniformity.

The retained target is `PhaseAwareVaughanTypeIIMinorArcPowerSaving`. It must preserve bilinear phase and be proved independently of the observed target correlation. TICKET111 proves none of the four conjectures.

## TICKET-112: Farey-cell endpoint Abel audit

TICKET112 applies exact discrete Abel summation inside all 162 connected cells of the fixed `Q=32` minor mask. The Type II minor contribution becomes the sum of cell endpoint terms plus smooth within-cell phase-variation terms. The identity replays below tolerance through 2M.

At 2M, the Farey-Abel envelope is `1,280,365.2`, only 16.85% of TICKET111's phase-blind singleton envelope `7,596,484.2`. This substantial improvement is still insufficient: the known major-plus-Type-I-minor contribution is `929,258.9`, leaving lower bound `-351,106.4`.

The remaining loss is concentrated at cell endpoints. Endpoint absolute mass is `1,229,823.0`, or 96.05% of the Abel envelope; within-cell variation is `50,542.3`. Actual signed endpoint contribution is `+11,146.8`. Independent endpoint triangles are therefore discarded.

Applying the already-frozen `X^(-1/6)` factor only to endpoint mass leaves finite lower expression `770,014.6` at the 2M holdout. This is not an all-scale estimate.

The retained target is `UniformFareyCellEndpointCancellationForVaughanCrossSpectrum`. TICKET112 proves none of the four conjectures.

## TICKET-113: right-Farey-denominator endpoint audit

TICKET113 freezes one structural rule after the exploratory `X=262,144` row: assign every TICKET112 Abel endpoint to the denominator of its immediate right Farey boundary. All `q=2,...,32` are retained, giving 31 complex blocks from 162 cells. No sign, subset, weight, or exponent is fitted.

The exact identity is `sum_C E_C=sum_q D_q`, where `D_q` is the sum of endpoints whose right boundary has denominator `q`. Taking absolute values only after forming each `D_q` retains within-denominator phase cancellation. The unchanged Abel variation envelope is then added.

At the new 4M holdout, endpoint absolute mass is `2,161,424.6`, the 31-block endpoint envelope is `767,682.2`, variation costs `89,185.2`, and known major-plus-Type-I-minor is `1,874,243.5`. The resulting finite lower expression is `1,017,376.2`. Both the Abel identity and denominator grouping identity replay within `3.2e-9`.

This finite success does not establish uniformity. A countermodel replaces each endpoint by `-|E_C|` while preserving cell labels, group counts, magnitudes, and magnitude-only norms. It gives lower expression `-376,366.3` at 4M and fails closure on all six scales. Thus Farey labels and magnitudes alone are insufficient; any proof must use phase relations imposed by the actual Vaughan bilinear coefficients. The countermodel is not claimed to be Vaughan-realizable.

The retained target is `UniformRightFareyDenominatorEndpointBudgetForVaughanCrossSpectrum`. TICKET113 proves none of the four conjectures.

## TICKET-114: Ramanujan mean and centered-numerator dispersion

TICKET114 opens each TICKET113 right-denominator block by reduced numerator. If `P_{q,a}` is the unphased Abel endpoint coefficient for the cell immediately left of `a/q`, the endpoint phase is transferred to the exact rational phase `rho_{q,a}=exp(4 pi i a/q)`. The signed transfer error is retained exactly and bounded by `4 pi |P_{q,a}| |alpha-a/q|`.

Writing `Re(P_{q,a})=m_q+x_{q,a}` with `sum_a x_{q,a}=0` gives an exact rational-boundary decomposition. The mean contribution is `m_q c_q(2)/2` for `q>2` and `m_2 c_2(2)` for `q=2`. The remainder is the inner product of `(x_{q,a}, Im P_{q,a})` with `(cos(4 pi a/q)-mean(cos), -sin(4 pi a/q))`.

Cauchy-Schwarz gives the projected L2 support envelope. This bound is sharp under the stated weak contract: choosing the coefficient vector opposite to the projected phase vector attains the negative support value. This proves that no generic rearrangement or repeated Cauchy argument can improve the bound without adding arithmetic constraints. The abstract extremizer is not asserted to be Vaughan-realizable.

Across `X=4K,32K,262K,1M,2M,4M`, the signed-mean lower expression is positive on four scales and the stronger sign-free expression is positive only on the last three. At 4M the sign-free adverse budget is `82.50%` of the known major-plus-Type-I-minor term and leaves finite lower expression `327,951.0`. Small-scale failures are retained, so the terminal run is theorem-selection evidence rather than a uniform estimate.

The retained target is `EventuallySubcriticalVaughanCenteredFareyNumeratorDispersionBudget`. It must derive, from actual Möbius/divisor bilinear coefficients, a fixed-margin all-sufficiently-large-scale bound for the mean, centered, boundary-transfer, and variation envelopes. A valid negative result would be a Vaughan-realizable coefficient family violating that margin. TICKET114 proves none of the four conjectures.

## TICKET-115: complex cyclotomic mean and orientation no-go

TICKET115 writes every numerator endpoint block as `P_{q,a}=M_q+Z_{q,a}` with complex zero-sum `Z`, and retains the exact half-Farey phase sum `H_q=sum_a exp(4 pi i a/q)`. This gives the exact identity `Re sum P rho=Re(M_qH_q)+Re sum Z(rho-mean rho)` and the exact geometry `||rho-mean rho||_2^2=n_q-|H_q|^2/n_q`.

The complex-centered remainder has a sharp L2 support bound. Under only complex zero mean and a fixed norm, the negative conjugate projected phase attains equality. Any stronger theorem must therefore use actual Vaughan arithmetic.

The finite audit separates two contracts. Paying `sum_q |Re(M_qH_q)|` improves the TICKET114 numerator budget on all six scales and gives 4M lower expression `335,523.7`. Paying the orientation-free `sum_q |M_q||H_q|` worsens all six scales and gives only `248,127.1` at 4M; it also loses the 1M finite closure. Thus orientation-free complex centering is discarded.

The retained target is `EventuallySubcriticalVaughanCyclotomicMeanAndComplexCenteredNumeratorBudget`. It must prove a fixed-margin all-sufficiently-large-`X` estimate for the scalar cyclotomic mean, complex-centered projected norm, boundary transfer, and Abel variation, and must establish the positive comparison scale independently. TICKET115 proves none of the four conjectures.

## TICKET-116: Möbius-sign lift and polarization no-go

TICKET116 expands the actual Vaughan Type-II sequence into nonnegative outer-divisor layers `II=II_plus-II_minus`, separated by `mu(d)=+1` and `mu(d)=-1`. Linearity carries this identity through the DFT, fixed minor-cell prefix sums, and half-Farey endpoint map. Complex centering therefore gives `M=M_plus-M_minus` and `Z=Z_plus-Z_minus` for all 31 denominator blocks.

The exact centered polarization identity is `||Z||^2=||Z_plus||^2+||Z_minus||^2-2 Re<Z_plus,Z_minus>`. The covariance is negative on the first two audited rows and positive on the next four, so a favorable sign is not assumed. Bounding the two sign layers independently is deterministically weaker by triangle inequality and empirically worsens all six rows. At 4M, the numerator budget grows from `1,449,516.0` to `4,187,038.4`, and the finite lower expression changes from `335,523.7` to `-2,401,998.7`.

Independent Möbius-sign triangles are therefore discarded. The retained target is `EventuallySubcriticalSignedVaughanMobiusCyclotomicDispersionBudget`: derive the endpoint estimate from the signed outer-Möbius bilinear sum before norms, or prove a denominator-summed covariance lower bound strong enough to preserve a fixed all-sufficiently-large-scale margin. An unbounded sequence of actual Vaughan layers violating every such margin would refute this target. TICKET116 proves none of the four conjectures.

## TICKET-117: signed dyadic endpoint Gram and adjacent-pair frontier

TICKET117 partitions the actual outer-divisor range into truncated dyadic shells while retaining `mu(d)` inside every shell. It verifies `II=sum_B II_B` in time and carries the identity through the DFT, fixed minor cells, and half-Farey endpoint map. For each denominator, complex centering gives the exact real-Gram identity `||Z_q||^2=sum_(B,C) Re<Z_q^(B),Z_q^(C)>`.

Singleton dyadic triangles are weaker than the fully signed budget on all six rows and close none. They do recover cancellation lost by TICKET116: at 4M the numerator budget falls from the separated-sign value `4,187,038.4` to `2,325,858.6`. Denominator Cauchy collapse also closes no row. Geometry-weighted off-diagonal Gram energy is net reinforcing on all six rows, with the largest 4M interactions concentrated among the low outer-divisor shells.

The audit then exhausts every horizon-wide contiguous partition with at most two adjacent shells per group. It never chooses a different partition by denominator. At 4M the optimum `(D128,D256),(D512,D1024),(D2048,D4096),(D8192,D16384)` reduces the numerator budget to `1,786,276.0`; the finite lower expression is `-1,236.3`. The same partition appears at 2M. This near closure and apparent stability are finite selected evidence, not a proof. The first pair contributes 51.8% of the paired budget.

Separate sign triangles, singleton dyadic triangles as a terminal bound, denominator Cauchy as a closure mechanism, and eventual-stability inference are discarded. The retained target is `EventuallySubcriticalAdjacentDyadicPairVaughanEndpointBudget`: prove a denominator-summed signed bilinear estimate for a non-data-selected adjacent-pair rule and a fixed all-sufficiently-large-scale margin below an independently positive comparison term. An unbounded Vaughan-realizable sequence violating every such margin is the counterexample route. TICKET117 proves none of the four conjectures.

## TICKET-118: preregistered canonical adjacent-pair holdout

TICKET118 separates rule selection from evaluation. Commit `5b52d4d58873afc512555ba6079d4280f61757ae` was pushed before the result artifact existed. It froze `X=8,388,608`, consecutive pairing of increasing nonempty outer-divisor dyadic shells, one partition for all 31 Farey denominators, no post-result optimization, and strict positivity of the finite lower expression as the primary endpoint.

The primary endpoint passes. At 8M, fully signed numerator budget is `2,858,354.9`, canonical adjacent-pair budget is `3,412,519.6`, boundary and variation cost `158,135.8`, known major-plus-Type-I-minor is `3,727,382.4`, and the finite lower expression is `+156,727.0`. The canonical partition equals the post-hoc best width-two partition, but this is recorded only as a secondary check.

The first canonical group, spanning actual outer divisors 204-511, contributes 46.84% of the paired budget. Thus the next proof object is no longer an empirically selected partition: it is a fixed factor-four signed Möbius/divisor block family. One holdout pass does not establish eventual closure, and no finite trend is promoted to a theorem.

The retained target is `EventuallySubcriticalCanonicalAdjacentDyadicPairVaughanEndpointBudget`. Prove a denominator-summed bilinear endpoint bound for every canonical group with a fixed all-sufficiently-large-scale margin and prove positivity of the comparison term on the same range. An unbounded Vaughan-realizable scale sequence violating every fixed margin would refute the target. TICKET118 proves none of the four conjectures.
## TICKET-122: Canonical joint scalar-vector defect audit

TICKET-122 extends the TICKET-121 first-pair centered certificate to every result-independent canonical adjacent dyadic pair and includes the scalar block means. For each Farey denominator it proves the exact identity

```text
|m0|+|m1|-|m0+m1| + w(a+b-||z0+z1||)
 = 2*1_{m0*m1<0}*min(|m0|,|m1|)
   + 2w(ab-Re<z0,z1>)/(a+b+||z0+z1||).
```

The identity yields a denominator-summed joint lower certificate. It also exposes two necessary global conditions. A perfectly cancelling first pair can have vanishing global mass beside arbitrarily large aligned outer pairs, and complete centered cancellation can be diluted by arbitrarily large same-sign scalar means. Thus both `first-pair-only` and `centered-only` full-budget routes are formally discarded.

The finite audit covers 8 scales, 28 canonical pair groups, and 868 pair-denominator rows. Exact global saving is at least `19.3458%`, the joint lower certificate is at least `16.0000%`, the maximum reconstruction error is `9.32e-10`, and machine failures are zero. Only 8M and 16M have positive complete finite margins. The 16M exact saving fraction is lower than 8M, so no monotonicity or asymptotic lower bound is claimed.

Retain `VaughanCanonicalPairJointDefectAndResidualBudgetGap`. It must prove, for fixed `delta>0` and every sufficiently large `X`,

```text
known_without_type_ii_minor
  - canonical_paired_budget
  - boundary_and_variation
  >= delta * known_without_type_ii_minor.
```

The matching negative route is an unbounded Vaughan-realizable sequence with nonpositive or vanishing normalized surplus. TICKET-122 proves no conjecture and certifies no conjecture counterexample.

## TICKET-123: canonical defect ratio closure bridge

Let `K>0` be the independently positive comparison budget, `S` the independent singleton budget, `E` the boundary-and-variation budget, and `D` the exact canonical pair saving. TICKET-123 proves the exact normalization

```text
[K-(S-D)-E]/K = 1-(1-eta)rho-epsilon,
eta=D/S, rho=S/K, epsilon=E/K.
```

It also proves `CanonicalDefectRatioClosureBridge`: if fixed constants satisfy `0<=eta<=1`, `D>=eta*S`, `S<=rho*K`, `E<=epsilon*K`, and `(1-eta)rho+epsilon<=1-delta`, then `K-(S-D)-E>=delta*K`.

Four explicit families eliminate incomplete arguments. A fixed positive saving fraction is defeated by unbounded `S/K`; bounded `S/K` is defeated by an unbounded boundary ratio; equality in the compatibility plane gives zero margin; and an arbitrary finite pass prefix can be followed by a failing unseen row. These refute auxiliary proof routes, not Twin Prime.

The inherited eight-scale ledger has two exact closures and one certificate closure. All normalized identities reproduce below `2.23e-16`. From 8M to 16M, the exact margin change `+0.155274` decomposes into eta `-0.038066`, rho `+0.189393`, and epsilon `+0.003947`. The finite improvement is therefore driven by lower `S/K`, not stronger canonical saving. No monotonicity or asymptotic bound is inferred.

The next Twin target is `VaughanCanonicalDefectRatioTriple`: prove one compatible constant tuple for every sufficiently large scale, or build a Vaughan-realizable escaping sequence. RH finite Jensen hyperbolicity, Collatz finite stopping-time or density evidence, and Goldbach mean singular-series agreement are explicitly discarded as infinite proof proxies while their independent targets are preserved. TICKET-123 proves no conjecture and certifies no conjecture counterexample.

## TICKET-124: canonical obstruction limsup criterion

TICKET124 corrects the next target chosen by TICKET123. Define the exact joint obstruction

```text
Q_X=((S_X-D_X)+E_X)/K_X=(1-eta_X)rho_X+epsilon_X.
```

The normalized route margin is exactly `delta_X=1-Q_X`. Therefore there are fixed `delta>0` and `X_0` with `delta_X>=delta` for every `X>=X_0` if and only if `limsup Q_X<1`. The forward direction is immediate from `Q_X<=1-delta`; for the reverse direction, if `L=limsup Q_X<1`, choose `delta=(1-L)/2` and use the definition of limsup.

The prior `VaughanCanonicalDefectRatioTriple` is sufficient but not necessary. Alternating `(eta,rho,epsilon)=(1/5,1,0)` and `(1,1,4/5)` gives `Q_X=4/5` and margin `1/5` at every scale, while every separate coordinate envelope has compatibility left side at least `8/5`. Also, `K=1,S=1/X,D=E=0` closes with no positive saving-fraction floor. These are exact auxiliary-target countermodels, not Twin Prime counterexamples and not claims about realizability by Vaughan coefficients.

The eight inherited finite rows have two exact closures and one certificate closure. The 16M exact obstruction is `0.802678` and certificate obstruction is `0.834379`, but these finite values do not estimate the true limsup. The corrected target is `VaughanCanonicalObstructionLimsup`: prove the joint tail bound arithmetically, preserving compensation, or produce a Vaughan-realizable unbounded subsequence with `Q_X>=1`. Exact-gap transfer and parity survival remain open.

The cross-problem audit also narrows scope. RH requires an exact all-test-function positivity contract. `GoldenMeanInvariantSetEscape` is retained only as a Mersenne-delay subroute and is not a sufficient Collatz bridge; the global target returns to `ResidueRankDescentCover`. Goldbach requires an explicit joint residual constant, positive major term, cutoff below the verified range, and finite glue. TICKET-124 proves no conjecture and certifies no conjecture counterexample.

## TICKET-125: four infinite bridge contracts

TICKET-125 converts each retained target into an exact conditional theorem and
adds countermodels for missing hypotheses. For RH, continuous quadratic-form
positivity on a dense cone extends to the completed test space; nondense,
discontinuous, and finite-Gram variants fail exactly. The open work is the
problem-specific density, continuity, and non-circular positivity theorem.

For Collatz, universal finite stopping descent is equivalent to the conjecture
by strong induction. The lifted-cylinder identity
`T^m(r+2^k t)=T^m(r)+3^m 2^(k-S)t` certifies every lift whenever descent occurs
before `S=k`. At 18 bits, 121,825 of 131,072 odd cylinders are certified and
9,247 remain. The residue `-3^(-1) mod 2^k` forces a refinement boundary at
every fixed precision, so the next target is adaptive rather than a fixed
finite quotient.

For Goldbach, weighted prime-pair positivity follows from explicit constants
`A,K,B` satisfying
`A-K/log(H)-B log(H)^2/sqrt(H)>0` at the verified `H=4e18`. The monotone-tail
and finite-glue proof is exact; the constants remain unproved. For Twin Prime,
the affine recurrence `Q_(2X)<=alpha Q_X+beta`, with
`alpha+beta<1`, implies dyadic `limsup Q<=beta/(1-alpha)`. The frozen finite
candidate `(alpha,beta)=(3/4,23/100)` passes four selected transitions but has
no holdout, no uniform Vaughan proof, and no between-scale interpolation.

TICKET-125 proves no conjecture and certifies no conjecture counterexample. The
next targets are `AdmissibleKernelConeDensityAndPositivity`,
`AdaptiveResidueFiniteStoppingCover`, `ExplicitJointBalancedGoldbachCutoff`,
and `DyadicVaughanObstructionContractionAndInterpolation`.

## TICKET-126: route correction and one closed premise

TICKET-126 tests the TICKET-125 contracts against their actual mathematical
domains. For RH, `ContinuousEvaluationSeparatesAutocorrelationCone` proves an
exact no-go: every real autocorrelation has nonnegative value at the identity,
so continuous identity evaluation separates its cone from any
negative-at-identity test function. Full-test-space autocorrelation density is
discarded. This does not refute Weil's criterion or RH; the retained target is
direct `NonCircularWeilAutocorrelationPositivity` on the exact admissible class.

For Collatz, an ordinary positive integer is precisely an inverse-limit residue
path that eventually always selects the low lift. The theorem
`EventuallyLowUnresolvedPathIffFiniteStoppingCounterexample` identifies finite
stopping counterexamples exactly with eventually-low infinite paths in the
adaptive unresolved tree. The compatible `-3^(-1)` boundary ray is not such a
path and is removed as a natural-number obstruction. At 28 bits the exact
audit leaves 4,027,110 of 134,217,728 odd classes unresolved, mass
`0.0300043076276779`, and observes a longest low run of 24. Those finite facts
do not exclude an infinite path.

For Goldbach, the number of distinct proper prime powers satisfies

```text
Q(N) <= sqrt(N) + (floor(log_2 N)-2) N^(1/3).
```

Consequently their weighted contamination is bounded by

```text
2 sqrt(N) log(N)^2 [1+(log_2 N-2)N^(-1/6)].
```

Monotonicity above 1614 gives the uniform endpoint constant
`B=2.0949181787429647` at `H=4e18`. This closes one previously open premise;
explicit pointwise major and signed-residual constants `A,K` remain open.

For Twin Prime, the preregistered 32M finite transition passes without
parameter retuning. Its certified obstruction is `0.771657434492807`, and the
frozen affine residual is `0.145872900933948<0.23`, leaving slack
`0.0841270990660519`. The failed first execution and tolerance-only recovery
preregistration are preserved in the provenance record. Five finite passes do
not imply a uniform recurrence, all-X interpolation, parity survival, or a
positive exact-gap-two lower bound.

TICKET-126 proves three intermediate theorems and records one finite holdout.
It proves no conjecture and certifies no conjecture counterexample. The next
targets are `NonCircularWeilAutocorrelationPositivity`,
`UniformNontrivialEventuallyLowPathExclusion`,
`ExplicitGoldbachMajorAndResidualConstants`, and
`DyadicVaughanObstructionContractionAndInterpolation`.

## TICKET-127: exception repair and effective bridges

TICKET-127 first repairs a public logical defect. The fixed Collatz path `n=1`
is eventually low and has no strict descent, so TICKET126's original statement
that all eventually-low paths must be absent was impossible. The exact path
equivalence remains valid, but its Collatz corollary is restricted to `n>1`.
At 28 bits there are 4,027,109 nontrivial unresolved odd classes after removing
the one fixed path; the longest nontrivial low runs have length 23 with
witnesses 27 and 31.

For RH, continuity plus a dense enumerable core proves completeness of strict
negative-witness search, conditional on exact interval evaluation. This is a
counterexample semidecision theorem, not a finite proof route. For Goldbach,
the binary singular series satisfies `S(N)>=1` by comparison with the
telescoping product over all integers. In the exact identity
`R(N)=G(N)-S(N)N`, this closes normalized `A=1` and isolates the still-open
pointwise residual constant `K<42.83274372223497` above `H=4e18`.

For Twin Prime, the normalized dyadic recurrence is exactly equivalent to a raw
Vaughan adverse-numerator transport inequality. The 16M-to-32M audit separates
the normalized residual into paired contribution 0.14135151084290043 and
boundary contribution 0.004521390091047683. These identities define a sharper
coefficient-level target but prove no tail recurrence or parity breakthrough.

TICKET-127 proves four intermediate statements and records one historical
correction. All conjecture-resolution counters remain zero. The next targets
are `IntervalCertifiedWeilCoreEvaluator`,
`UniformNontrivialEventuallyLowPathExclusion`,
`ExplicitPointwiseBinaryGoldbachResidualConstant`, and
`UniformVaughanRawBudgetTransportAndInterpolation`.

## TICKET-131: proof viability and target correction

TICKET131 audits whether the TICKET130 targets actually reduce the four infinite
problems. It proves a finite-dimensional positivity no-go for RH: every proper
finite audited subspace admits two continuous quadratic forms that agree there
while one is negative on an orthogonal direction. Finite Gram or Galerkin
positivity therefore needs a Weil-specific tail theorem before it can support a
universal conclusion.

For Collatz, the ticket corrects a scope error. TICKET129 proves the strict
valuation cap only through `2H=2^29`, where `H=2^28`. The exact all-time
least-counterexample envelope contains the factor `(1+1/(3H))^j`, and at
`j=3H` the binomial theorem gives a value greater than two. Excluding all
infinite strict-cap paths is therefore not a sufficient target. The replacement
theorem proves that an infinite exact valuation word is generated by one fixed
positive integer if and only if its canonical nested start residues eventually
stabilize. The new target is
`NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope`.

For Goldbach, the singular-series factor gives an exact arithmetic
stratification. On even integers with an odd prime divisor at most 103, a
classwise residual estimate with `K=57` is sufficient; the exact endpoint margin
at 103 is `98007974997/216140000000000`. This covers a natural-density fraction
about `0.764061` of even integers but proves no residual estimate. The retained
target is `PointwiseBinaryGoldbachResidualByRoughnessStratum`.

For Twin Prime, `(a-k)/(1+k)=Q_X/Q_Y-1` proves that the TICKET130 target
`R<2/23` is exactly the within-block ceiling `Q_X/Q_Y<25/23`. It is a useful
normalization but no independent reduction in analytic difficulty. The route
returns to actual signed Vaughan coefficient transport and keeps parity as a
separate bridge: `UniformSignedVaughanBlockTransportWithParityBridge`.

TICKET131 proves five exact intermediate or route-correction statements. It
proves none of the four conjectures and certifies no conjecture counterexample.
# TICKET-132 continuation: admissibility and pointwise boundary theorems

TICKET-132 preserves every valid TICKET-131 theorem and narrows four proof
routes without claiming a conjecture solution. The machine-readable audit is
`data/open-problem/ticket132-admissibility-nullset-hard-stratum-local-parity.json`.

For RH, the TICKET-129 rational-bump core is projected onto the two exact moment
kernels with anchors `b(x)` and `b(x-1)`. The normalized moment determinant is
`e^(-1/2)-e^(1/2)<0`, so the projected computable core is countable and dense in
the admissible subspace. The next target is
`NonnegativeProjectedWeilCoreCertificate`; positivity itself is not proved.

For Collatz, natural valuation codes are countable and dense because every
finite exact cylinder contains all starts `r+kM`, but they have measure zero
under every non-atomic probability. Combined with TICKET-131, every natural
code is eventually residue-stabilizing. This exact dense-null theorem blocks
both finite-prefix separation and mass-only proof routes. The next target is
`PointwiseArchimedeanDescentOnDenseNullNaturalCodes`.

For Goldbach, `N=2^m` has empty odd-prime singular-series product and hence
normalized multiplier one for every `m`. Powers of two are an unavoidable
infinite minimal-main stratum, so finite small-divisor stratification is only a
workload reduction. The next target is
`PointwiseBinaryGoldbachResidualK56OnPowersOfTwoAndRoughStrata`.

For Twin Prime, CRT constructs, at every finite sieve level, an infinite
progression of small-prime-clean pairs with both entries composite. This is a
countermodel to finite-local primality certification, not to Twin Prime. The
next target is `UnboundedTypeIIParitySensitiveExactGapCertificate`.

All four conjectures remain open. TICKET-132 exact theorem count is four,
route-correction count is four, and conjecture-resolution count is zero.

# TICKET-133 continuation: exact quantifier-promotion reductions

TICKET-133 preserves every valid TICKET-132 theorem and proves four new exact
reduction or countermodel statements. The machine-readable audit is
`data/open-problem/ticket133-quantifier-promotion-exact-reductions.json`.

For RH, continuity and density make universal positivity on the projected core
equivalent to every finite rational Gram inequality. A strict negative witness
has a finite rational Gram certificate. The next target is
`IntervalCertifiedProjectedWeilGramFamily`; no finite initial segment proves RH.

For Collatz, a contracting valuation word has an exact finite non-descent set in
its natural residue cylinder. The audited 3,861 contracting cylinders have only
the unique exception `n=1`, while 44 noncontracting cylinders remain. The next
target is `PrefixFreeContractingCylinderCoverOfEveryNaturalCode`.

For Goldbach, an exact abstract residual spike supported on powers of two passes
every fixed finite Cesaro `L^p` average while reversing the K=56 endpoint margin
at every power. This refutes an average-to-pointwise inference, not Goldbach.
The next target is `HardStratumMaximalBinaryGoldbachResidualK56`.

For Twin Prime, every admissible residue class modulo a fixed finite primorial
has an infinite composite-composite CRT lift. The next target is
`UnboundedParitySensitiveTwinPairSeparation`; fixed-modulus classifiers are
insufficient.

All four conjectures remain open. TICKET-133 exact theorem count is four,
route-correction count is four, and conjecture-resolution count is zero.

# TICKET-134 continuation: uniformity thresholds and scale no-go theorems

TICKET-134 preserves every valid TICKET-133 result and proves four stronger
interval or scale-boundary statements. The machine-readable audit is
`data/open-problem/ticket134-uniformity-thresholds-and-scale-no-go.json`.

For RH, convergent rational entry intervals finitely certify every strict
positive-definite finite Gram matrix after a rational congruence preconditioner,
or every matrix with a negative direction through a rational witness. Singular
PSD matrices and the universal Gram tail remain undecided. The next target is
`UniformProjectedWeilGramTailCertificate`.

For Collatz, no finite or globally bounded-depth contracting-prefix family can
cover all natural starts. At every depth `K`, the exact cylinder
`n=-1 mod 2^(K+1)` has expanding all-one prefixes through depth `K`. The next
target is `WellFoundedUnboundedContractingPrefixCover`.

For Goldbach, the exact `L^(p_X)` norm of a fixed power-of-two spike has a
transition at `p_X` comparable to `log(N_X/J_X)`. Every sublogarithmic moment
regime can miss the pointwise obstruction. The next target is
`LogScaleMomentOrMaximalGoldbachResidualK56`.

For Twin Prime, every admissible `a mod W` has a composite-pair lift below
`2Wqr`. The obstruction therefore extends to growing residue-only classifiers
with `z(X)<=(1-epsilon)log X`. The next target is
`NearFullScaleParitySensitiveTwinSeparation`.

All four conjectures remain open. TICKET-134 exact theorem count is four,
route-correction count is four, and conjecture-resolution count is zero.

# TICKET-135 continuation: conditional bridges and exceptional-set boundaries

TICKET-135 preserves every valid TICKET-134 result and proves four exact
conditional bridge or no-go theorems. The machine-readable audit is
`data/open-problem/ticket135-conditional-bridges-and-exceptional-set.json`.

For RH, `SharpBlockTailPositivityCertificate` proves the dimension-independent
Schur-margin condition `beta^2<=alpha*gamma` and gives a sharp scalar negative
countermodel when it is violated. The next target is
`ProjectedWeilBlockConstantsWithPositiveSchurMargin`; no actual Weil constants
are supplied by the generic theorem.

For Collatz, `MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover` proves
an almost-everywhere statement in odd 2-adic code space. It does not cover every
natural code and does not dominate the positive affine iterate term. The next
target is `NaturalCodesCrossAffineDescentThreshold`.

For Goldbach, `SparseHardStratumMomentToMaximumBridge` proves the sharp finite
inequality and lowers the sufficient moment order to `O(log log X)` on a
powers-of-two-size hard stratum. The next target is
`BinaryGoldbachHardStratumLogMomentBoundK56`; the actual residual estimate is
open.

For Twin Prime, `FiniteCongruenceTranscriptCompositeLift` constructs proper
composite-pair witnesses below `2*lcm(m_i)*q*r` for arbitrary finite compatible
modular transcripts. The next target is `NonCongruenceTypeIITwinSeparation`.

한국어 요약: TICKET-135는 일반 조건부 승격 정리와 실제 난제에 필요한 입력을
분리했다. RH에는 실제 Weil 블록 상수, Collatz에는 모든 자연수 코드의 affine
하강, Goldbach에는 실제 hard-stratum residual 모멘트, Twin Prime에는 유한 합동
정보 밖의 Type II 분리가 남아 있다. 네 난제는 모두 미해결이고 해결 카운트는
0이다.

All four conjectures remain open. TICKET-135 exact theorem count is four,
route-correction count is four, and conjecture-resolution count is zero.

# TICKET-136 continuation: scale-sensitive obstructions and affine descent

TICKET-136 preserves the valid TICKET-135 bridges, closes four subordinate
lemmas, and narrows the next premise in each proof DAG. The machine-readable
audit is
`data/open-problem/ticket136-scale-sensitive-obstructions-and-affine-bridge.json`.

For RH, `SchurTestWeilBlockBridgeAndEntrywiseDecayNoGo` turns absolute
row/column sums into a usable cross-operator bound and proves with `J_n/n` that
entrywise decay alone is insufficient. The next target is
`ProjectedWeilAbsoluteRowColumnTailBoundsWithPositiveMargin`.

For Collatz, `LeastCounterexampleAffineCorrectionInequality` proves that
non-descent through depth `k` forces `2^S*n^k<=(3n+1)^k`. The strict reverse
inequality is an exact descent certificate. The next target is
`UniformValuationSurplusBeyondAffineCorrectionForLeastCounterexampleCodes`.

For Goldbach, `FixedWheelRoughStratumHasLinearMassAndLogMomentBarrier` proves
`|H_W(2WM)|=M*phi(W)` and blocks the extension of the powers-of-two
`O(log log X)` moment scale to a fixed-wheel linear-density stratum. The next
target is `BinaryGoldbachGrowingWheelResidualBoundK56`.

For Twin Prime, `FiniteRationalFourierAlgebraCompositeLift` proves that every
finite rational Fourier feature family remains a finite congruence transcript.
The next target is `AperiodicScaleGrowingTypeIITwinSeparation`.

한국어 요약: RH의 원소별 감소, Collatz의 기울기 수축, Goldbach의 희소층
모멘트 차수 확대, Twin Prime의 유한 유리 Fourier 분리 경로를 각각 정확한
반례 또는 필요조건으로 교정했다. 네 난제는 모두 미해결이며 해결 카운트는
0이다.

All four conjectures remain open. TICKET-136 exact theorem count is four,
route-correction count is four, proof-DAG count is four, and
conjecture-resolution count is zero.

# TICKET-137 continuation: cancellation, entropy, and information budgets

TICKET-137 preserves every valid TICKET-136 theorem while rejecting four
remaining overstrong inference routes. The machine-readable audit is
`data/open-problem/ticket137-cancellation-entropy-and-information-budget.json`.

For RH, `HadamardCancellationSchurOverestimateNoGo` proves that
`B_N=H_N/N` has absolute Schur product `R*S=1` but true squared operator norm
`1/N`. Absolute row and column sums are therefore sufficient but can be
arbitrarily too strong. The next target is
`ProjectedWeilSignedCrossBlockCancellationWithPositiveMargin`.

For Collatz, `AffineCappedValuationCylinderMassDecay` gives the exact Haar mass
of valuation words satisfying the TICKET-136 affine cap and proves exponential
decay. Every finite cylinder still contains arbitrarily large positive
integers, so measure zero cannot be promoted to arithmetic emptiness. The next
target is `ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet`.

For Goldbach, `SubpowerGrowingWheelLogMomentBarrier` proves that every odd
squarefree `W<=X^(1-epsilon)` leaves a polynomial-size hard stratum and still
requires `p=Omega(log X)` for worst-case moment promotion. The next target is
`NearFullScaleWheelOrPointwiseBinaryGoldbachResidualK56`.

For Twin Prime, `RationalFourierInformationBudgetLowerBound` proves that a
rational Fourier denominator lcm `L` has an in-range proper composite-pair
collision whenever `2Lrs<=X`. The next target is
`IrrationalOrSupercriticalAperiodicTypeIITwinSeparation`.

한국어 요약: 절댓값 크기는 RH의 부호 상쇄를, 작은 측도는 Collatz의 자연수
공집합을, 낮은 모멘트는 Goldbach의 점별 양성을, 유한 유리 주기는 Twin
Prime의 인수 민감 정보를 보존하지 못한다. TICKET-137은 이 네 손실을 정확한
정리로 확정하고 다음 보조정리를 수정했다. 네 난제는 모두 미해결이며 해결
카운트는 0이다.

All four conjectures remain open. TICKET-137 exact theorem count is four,
route-correction count is four, proof-DAG count is four, and
conjecture-resolution count is zero.

# TICKET-138 continuation: correlation, periodicity, and scale closure

TICKET-138 preserves every valid TICKET-137 theorem while rejecting four
remaining representational shortcuts. The machine-readable audit is
`data/open-problem/ticket138-correlation-periodicity-and-scale-closure.json`.

For RH, `CrossGramCorrelationBlockPositivityCriterion` proves
`||B||^2<=d+c`, where `d` is maximum row energy and `c` is the maximum
off-diagonal signed Gram-correlation budget. Balanced rank-one sign matrices
prove that zero signed row and column means do not control the operator norm.
The next target is
`ProjectedWeilCrossGramCorrelationBudgetBelowTailGap`.

For Collatz,
`SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding` derives
the exact periodic 2-adic start `n=C/(2^S-3^k)` and excludes every periodic
code with `2^S<=3^k` from positive natural embedding. The next target is
`AffineCappedNaturalCodeWellFoundedness`.

For Goldbach, `AllScaleOddSquarefreeWheelMomentBarrier` strengthens the
subpower result to every complete-block wheel scale:
`|H_W(X)|>=sqrt(X/2)`. Near-full wheel size alone therefore does not avoid
`p=Omega(log X)` worst-case promotion. The next target is
`PointwiseSignedBinaryGoldbachResidualK56`.

For Twin Prime,
`IrrationalInjectivityWithoutRegularityIsTautologicalNoGo` proves that every
integer predicate factors through an injective irrational phase by an
unrestricted lookup. Injectivity alone supplies no regular arithmetic
estimate or parity break. The next target is
`RegularAperiodicTypeIICancellationWithPositiveTwinMass`.

한국어 요약: TICKET-138은 평균 부호 상쇄를 cross-Gram 상관으로, Collatz
무한 언어를 정확 주기 고정점으로, wheel 크기 선택을 전 규모 하한으로,
무리수 feature 표현력을 계산 가능한 analytic regularity 문제로 교정했다.
네 난제는 모두 미해결이며 해결 카운트는 0이다.

All four conjectures remain open. TICKET-138 exact theorem count is four,
route-correction count is four, proof-DAG count is four, and
conjecture-resolution count is zero.

# TICKET-139 continuation: uniformity, Diophantine windows, and complexity

TICKET-139 preserves every valid TICKET-138 theorem while testing whether its
remaining sufficient conditions are dimension-sharp or uniform enough. The
machine-readable audit is
`data/open-problem/ticket139-uniformity-diophantine-complexity.json`.

For RH, `TwoMutuallyUnbiasedBasesCrossGramL1NoGo` constructs a Parseval tight
frame from two mutually unbiased bases. Its exact squared operator norm is one,
but its absolute cross-Gram bound is `(1+sqrt(N))/2`. The next target is
`ProjectedWeilSignedGramSpectralRadiusBelowTailGap`.

For Collatz, `CollatzCycleDiophantineWindowAndVerifiedFloorExclusion` proves
the exact positive-cycle window
`1 < 2^S/3^k <= (1+1/(3m))^k`. With the project's verified `m>=2^28` floor,
exact integer arithmetic excludes 19,999 of the first 20,000 period windows.
Period 15,601 is only unexcluded by this necessary condition. The next target
is `AllPeriodSupercriticalCycleDiophantineExclusion`.

For Goldbach, `PowerOfTwoBarycentricMomentAnnihilatorNoGo` uses Lagrange
barycentric weights to build a nonzero signed signal on powers of two with its
first `q` polynomial moments exactly zero for every finite `q`. The next target
is `LocalizedPowerOfTwoSignedGoldbachResidualK56`.

For Twin Prime, `FiniteIrrationalOrbitLipschitzLookupComplexityNoGo` proves
upper and lower Lipschitz interpolation bounds in terms of the orbit's minimum
separation. A regularity budget allowed to grow with inverse separation still
contains arbitrary finite lookup. The next target is
`UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass`.

한국어 요약: TICKET-139는 RH의 절댓값 cross-Gram 경계가 상쇄를 무한히
과대평가할 수 있음을 보이고, Collatz 양의 주기 궤도에 정확한 디오판토스
창을 부여하며, Goldbach의 유한 모멘트만으로 점별 양성을 추론할 수 없음을
거듭제곱 2 지지 신호로 증명하고, Twin Prime의 무리수 표현에는 규모와
무관한 정칙성 예산이 필요함을 정량화한다. 어느 결과도 네 추측의 완전한
증명이나 반례가 아니다.

All four conjectures remain open. TICKET-139 exact theorem count is four,
route-correction count is four, proof-DAG count is four, and
conjecture-resolution count is zero.

# TICKET-140 continuation: spectral moments, fixed-floor limits, duality, and rotation

TICKET-140 preserves every valid TICKET-139 theorem while replacing four
remaining qualitative targets by exact quantitative contracts. The
machine-readable audit is
`data/open-problem/ticket140-spectral-moments-fixed-floor-duality-rotation.json`.

For RH, `EvenTraceMomentSpectralCertificateAndLogOrderBarrier` proves
`rho(E)^(2m)<=tr(E^(2m))<=r rho(E)^(2m)` and turns even trace moments into a
signed positivity certificate. The identity family proves fixed-factor
control needs `m=Omega(log r)`. The next target is
`ProjectedWeilLogOrderEvenTraceMomentBelowTailGap`.

For Collatz, `FixedCycleMinimumWindowEventuallyVacuousNoGo` proves that the
fixed-floor product window exceeds factor two for every
`k>=ceil(7(3M+1)/10)`, so it then admits the canonical valuation sum at every
period. The next target is
`PeriodDependentCycleMinimumDiophantineSeparation`.

For Goldbach,
`FiniteMeasurementDualCertificateAndPowerOfTwoNullspaceNoGo` characterizes
pointwise information by membership of the evaluation functional in the
measurement row space. The next target is
`ArithmeticK56DualCertificateOnPowerOfTwoHardStratum`.

For Twin Prime, `QuadraticIrrationalSobolevRotationCancellation` proves
sample-length-uniform cancellation for unweighted mean-zero Sobolev
observables along the `sqrt(2)` rotation. The next target is
`DiophantineSobolevTypeIIBilinearCancellationWithPositiveTwinMass`.

한국어 요약: TICKET-140은 RH의 signed spectral norm을 로그 차수 trace
moment 문제로, Collatz의 고정 최솟값 창을 period-dependent minimum
문제로, Goldbach 점별 추정을 exact dual certificate 문제로, Twin Prime
무리수 정칙성을 arithmetic Type II 가중 상쇄 문제로 바꾼다. 네 결과는
정확한 부분정리 또는 no-go지만 어느 추측의 완전한 증명이나 반례도 아니다.

All four conjectures remain open. TICKET-140 exact theorem count is four,
route-correction count is four, proof-DAG count is four, and
conjecture-resolution count is zero.
# TICKET-145 continuation: normalization and separability no-go audit

Machine record:
`data/open-problem/ticket145-normalization-affine-endpoint-separable-no-go.json`.
Full bilingual proof:
`docs/normalization-affine-endpoint-separable-no-go.md`.

TICKET-145 re-audits the four open nodes proposed by TICKET-144 before treating
them as genuine progress. It proves:

1. `SchurPivotBasisScalingNoGoAndNormalizedAngleReduction`: absolute pivots
   are basis-scale dependent, and positive Hilbert sections refute the
   necessity of a uniform normalized pivot margin.
2. `FiniteModulusPiecewiseAffineCollatzRankNoGo`: the exact family
   `4Mk-1 -> 6Mk-1` defeats every lower-bounded finite-modulus
   piecewise-affine one-step rank.
3. `SignedMartingaleEndpointEquivalenceAndAggregateCancellationNoGo`: the
   signed endpoint is the original pointwise residual, while aggregate level
   cancellation admits an exact size-57 spike.
4. `AdverseWalshSlackIdentityAndMinimalSeparableMajorantNoGo`: the adverse
   part is the smallest nonnegative separable majorant, but counts
   `(90,5,4,1)` have positive twin mass with `B=178>A00=100`.

한국어 경계: 이번 TICKET은 네 난제를 해결하지 않는다. TICKET-144의
다음 표적 중 좌표 의존적이거나 순환적이거나 과도한 조건을 정확히
폐기했다. 다음 단일 미증명 정리는 각각
`ExplicitWeilFormCoreNormalizedSchurSignRecurrence`,
`NonlinearLiftClosedCollatzRankBeyondFiniteResidueAffine`,
`ArithmeticBinaryGoldbachScaleEnvelopeSummableK56`,
`IndependentCubicRoughJointWalshTypeIIBound`이다. 완전 증명이나 추측의
반례가 없으므로 네 해결 상태는 모두 `open_not_proven`이다.

## TICKET-146 continuation: Toeplitz, polynomial, phase, and Frechet gates

TICKET-146 attacks the four TICKET-145 open targets without promoting finite
evidence to an infinite conclusion.

1. **Riemann Hypothesis.** Under the stated involution compatibility, a
   shift-generated Weil convolution-form core has an exact Hermitian Toeplitz
   Gram family. Its Schur pivots obey the Levinson recurrence
   `E_m=E_(m-1)(1-kappa_m^2)`. For every fixed lag `L`, moments identical to
   the identity through `L` can hide `kappa_(L+1)=-2` and pivot `-3`.
   This adversarial family belongs to the unrestricted Hermitian Toeplitz
   moment class and is not asserted to be Weil-realizable. Therefore generic
   fixed-lag recurrences without additional Weil structure are discarded.
   The next target is
   `ExplicitWeilShiftCoreReflectionCoefficientUnitDiskBound`.
2. **Collatz.** The same-residue family `4Mk-1 -> 6Mk-1` excludes every
   lower-bounded rank that is polynomial on each class of a fixed finite
   residue partition. Constant polynomials give equality and positive-leading
   polynomials eventually increase. The next target is
   `SymbolicCylinderAdaptiveBlockDescentBeyondPolynomialRanks`.
3. **Goldbach.** Translation preserves mean, cyclic autocorrelation, and all
   Fourier magnitudes but shifts a binary convolution endpoint by twice the
   translation. Thus power-spectrum-only envelopes cannot recover signed
   pointwise cancellation. The next target is
   `PhaseResolvedBinaryGoldbachScaleEnvelopeSummableK56`.
4. **Twin Prime.** Sharp Frechet bounds show that
   `(A00,A10,A01)=(100,0,0)` is compatible with both zero and positive twin
   mass. Separate marginal Liouville cancellation is insufficient. A
   sufficient one-sided budget is
   `A10<=epsilon_1 A00`, `A01<=epsilon_2 A00`,
   `A11>=-gamma A00`, with `epsilon_1+epsilon_2+gamma<1`. The next target is
   `CubicRoughOneSidedJointLiouvilleTypeIIMargin`.

한국어 경계: 이번 TICKET은 네 난제를 해결하거나 반증하지 않는다. RH의
실제 all-order reflection 계수, Collatz의 lift-closed adaptive block
descent, Goldbach의 phase-resolved 점별 K56 추정, Twin의 joint
Liouville Type I/II margin은 모두 미증명이다. 정확한 정리와 반례는
잘못된 증명 경로를 폐기하고 다음 보조정리를 더 좁히는 역할만 한다.

## TICKET-147 continuation: fiber, compensation, phase, and path-cut gates

TICKET-147 attacks the four TICKET-146 open nodes by separating completeness,
pointwise coverage, phase resolution, and arithmetic label information.

1. **Riemann Hypothesis.** Fourier fiberization proves that finitely many
   generators and every translate on one fixed lattice have fiber dimension
   at most the number of generators, while the ambient `L2(R)` fiber is
   infinite-dimensional. Finite fixed-lattice cores are therefore
   incomplete in `L2(R)`. The next target is
   `InfiniteMultiscaleWeilFiberCompletenessAndMatrixSchurBound`.
2. **Collatz.** If the first `r` accelerated valuations are one and the next
   valuation is `b>=r+2`, then the exact formula
   `T^(r+1)(n)=(3^(r+1)q-1)/2^(b-1)` proves strict descent for every positive
   `n>1` in that cylinder. These cylinders have exact relative odd-Haar mass
   `2/3`. The residual third contains infinite positive `b=2` families. The
   next target is `ResidualThirdIteratedRunCompensationRenewalDescent`.
3. **Goldbach.** Nearest `M`-sector quantization of the endpoint-aligned
   squared Fourier phase has error at most
   `22/(7M) sum_x |f(x)|^2`. The elementary Lambda energy bound requires
   `M>=ceil(11 log(N)^3/196)` merely to fit the quantization error inside
   `56N/log N`; fixed resolution plus Parseval is discarded. The next target
   is `ArithmeticPhaseSectorImbalanceBoundSummableK56`.
4. **Twin Prime.** The joint Liouville coefficient on a gap-two support graph
   is `A11=A00-2*Cut`. Paths with `4m` vertices admit alternating and
   single-block labels having the same `(A00,A10,A01)` but `A11` values
   `-(4m-1)` and `4m-3`. Unsigned topology and marginals cannot replace
   arithmetic label control. The next target is
   `CubicRoughLiouvillePathSwitchDeficitTypeIIBound`.

한국어 경계: Collatz의 `2/3`은 실제 pointwise 무한 가족 정리이지만 남은
`1/3` 때문에 추측의 증명이 아니다. RH 결과는 `L2` 완전성 no-go이며
실제 Weil topology를 자동으로 결정하지 않는다. Goldbach 결과는 위상
양자화 오차만 제어하고 sector별 산술 상쇄를 증명하지 않는다. Twin의
반례 label은 실제 Liouville 함수가 아니다. 네 해결 상태는 모두
`open_not_proven`이다.

## TICKET-148 continuation: multiscale, renewal, sharpness, and matching gates

TICKET-148 attacks the four TICKET-147 open nodes and records one required
scope correction.

1. **Riemann Hypothesis.** Unit-interval scaling functions and all dyadic
   Haar wavelets form a complete orthonormal basis of `L2(R)`. For every
   finite prefix, a bounded self-adjoint diagonal operator can be positive on
   the prefix and negative on the next basis vector. Multiscale completeness
   is therefore insufficient without an actual Weil-matrix tail bound. The
   next target is
   `SmoothWeilWaveletCoreAndUniformMatrixTailPositivityBound`.
2. **Collatz.** For every `L>=1`, all positive integers
   `2*8^L(1+t)-5` follow the accelerated valuation word `(1,2)^L` and map
   to `2*9^L(1+t)-5`, which is larger. This exact cylinder family rejects
   every universal fixed renewal horizon but does not give a divergent
   positive orbit. The next target is
   `AdaptiveRenewalRankEscapingMinusFiveTwoAdicShadow`.
3. **Goldbach.** For the nonnegative function
   `f(x)=1+cos(2*pi*x/q)`, with `q=4M^2` and
   `N=M^2+2M-1`, nearest-sector phase quantization satisfies
   `M*error/E -> pi/3`. Hence the TICKET-147 `O(E/M)` rate is
   order-sharp under generic positivity and energy assumptions. The next
   target is
   `VonMangoldtEndpointSectorCancellationBeyondSharpGeometricRate`.
4. **Twin Prime.** The actual TICKET-142 cubic-rough support is a matching
   for `X>=13`, because two adjacent gap-two edges would require three
   numbers spaced by two all to avoid the prime `3`. TICKET-147's general
   path identity remains true, but its long-path counterfamily is not
   realizable in that support. On a matching, correlated and anticorrelated
   labels still have identical endpoint marginals and opposite joint terms.
   The next target is
   `CubicRoughLiouvilleMatchingCouplingTypeIIBound`.

한국어 경계: 이번 TICKET은 완전 증명이나 네 추측의 반례를 제시하지
않는다. RH에서는 실제 Weil tail, Collatz에서는 adaptive shadow escape,
Goldbach에서는 von Mangoldt 고유 상쇄, Twin Prime에서는 실제 Liouville
matching coupling이 미증명이다. TICKET-147의 Twin 장경로 적용은
TICKET-148의 matching 정리로 명시적으로 교정되며, 일반 path-cut
항등식 자체는 유지된다.

## TICKET-149 continuation: smooth coercivity, exact escape, wheel residual, and semiprime cover

TICKET-149 attacks the four TICKET-148 open nodes while keeping the
resolution count at zero.

1. **Riemann Hypothesis.** A Schwartz-class Meyer wavelet system closes the
   requested smooth `L2` basis issue. Nevertheless, for every finite prefix
   and every `epsilon>0`, a finite-rank self-adjoint diagonal operator can be
   positive on the prefix, have absolute tail norm `epsilon`, and retain one
   negative direction. Smooth completeness and absolute compact-tail
   smallness are discarded as a positivity certificate. The next target is
   `ExplicitWeilWaveletCoerciveReferenceAndRelativeTailNormBelowOne`.
2. **Collatz.** For every positive odd `n`, the maximal initial
   minus-five shadow has exactly `floor((v2(n+5)-1)/3)` valuation pairs
   `(1,2)`. It exits in one of three exact terminal types, but every
   nonempty shadow exits above its entry value. Shadow escape alone is
   therefore not descent. The next target is
   `ThreeExitTypePostShadowAdaptiveDescent`.
3. **Goldbach.** Every even endpoint has an exact positive local convolution
   on every even squarefree wheel. Bilinearity gives an explicit residual
   transfer inequality, while a reduced-residue singleton proves that wheel
   support alone can still miss any prescribed endpoint. The next target is
   `VonMangoldtWheelResidualPointwiseBilinearSavingK56`.
4. **Twin Prime.** On the cubic-rough support, if `L,R` count semiprime left
   and right endpoints and `E` is total rough edge mass, then
   `twins>=E-L-R=-(A10+A01)/2`. Thus positive rough-edge mass together
   with a uniform deficit in `L+R` is an alternative sufficient route that
   does not require estimating the full joint term. The next target is
   `CubicRoughSemiprimeEndpointCoverDeficit`.

한국어 경계: RH의 작용소 반례는 실제 Weil 형식이 아니고, Collatz의
shadow 탈출은 전역 종료가 아니며, Goldbach의 wheel 공식은 실제
von Mangoldt residual을 제어하지 않고, Twin의 유한 cover 비율은 균일
`delta`를 증명하지 않는다. 네 추측은 모두 `open_not_proven`이다.

## TICKET-150 continuation: relative form, arbitrary delay, sharp holes, and parity equivalence

TICKET-150 attacks the four TICKET-149 open nodes and corrects which proposed
bridges are genuinely weaker than the target.

1. **Riemann Hypothesis.** For a positive reference form `P` and symmetric
   perturbation `K`, the relative operator
   `B=P^(-1/2)KP^(-1/2)` gives
   `P+K>=(1-||B||)P`. Norm at most one implies nonnegativity and the
   threshold is sharp. A positive compact reference cannot have a positive
   ambient `L2` spectral floor in infinite dimension. The next target is
   `ActualWeilPrimeArchimedeanRelativeFormBoundAtMostOne`.
2. **Collatz.** The `r=1` and `r=3` minus-five shadow exits contract below
   their exit value in at most two accelerated steps. The `r=2` exit instead
   admits, for every `L,H`, an exact positive CRT family with shadow
   `(1,2)^L` followed by `(1,1,1^H)`, all above the pre-shadow start.
   Every fixed post-shadow window is therefore retired. The next target is
   `TypeTwoAdaptiveValuationSurplusDescentBelowShadowEntry`.
3. **Goldbach.** If `g` is the reduced-residue indicator and
   `m=(g*g)(N)`, the exact minimum squared `L2` distance from `g` to a
   nonnegative endpoint-hole weight is `(m+h)/2`, where `h` counts fixed
   endpoint-reflection residues. This threshold is sharp, and its relative
   value tends to zero on primorial wheels at `N=2`. The next target is
   `VonMangoldtEndpointReflectionMassRetentionK56`.
4. **Twin Prime.** The TICKET-149 cover deficit is exactly
   `E-L-R=T-D=-(A10+A01)/2`, where `T` is the twin cell and `D` the
   double-semiprime cell. Thus the deficit is a parity-sensitive
   twin-versus-double-semiprime bias, not an unsigned shortcut. The next
   target is
   `PositiveCubicRoughMassAndOneSidedLiouvilleMarginalGap`.

한국어 경계: RH의 상대 form 정리는 실제 Weil 분해가 아니고, Collatz의
CRT 가족은 임의로 긴 유한 지연일 뿐 발산 궤적이 아니다. Goldbach의
sharp hole 가중치는 실제 von Mangoldt 함수가 아니며, Twin 등가식은
`A10+A01`을 무한 scale에서 추정하지 않는다. 네 추측은 모두
`open_not_proven`이고 해결 카운터는 0이다.

## TICKET-151 continuation: negative spectrum, affine thresholds, reflection transversals, and log-two selection

TICKET-151 sharpens each TICKET-150 open target while retaining zero
conjecture resolutions.

1. **Riemann Hypothesis.** For a relative self-adjoint operator `B`,
   positivity of the combined form is equivalent to `B>=-I`, or exactly
   `||B_-||<=1`. The full condition `||B||<=1` is sufficient but
   unnecessarily strong because arbitrarily large positive spectrum is
   harmless. The next target is
   `ActualWeilNegativeRelativeFormPartBoundAtMostOne`.
2. **Collatz.** Every realized finite valuation word has the exact affine
   form `(3^m n+C_m)/2^S`; descent is equivalent to
   `D=2^S-3^m>0` and `n>C_m/D`. The natural start `n=165` has positive
   `D` but maps to `167` after 17 accelerated steps, so surplus alone is
   insufficient. Every forced TICKET-150 type-two horizon has `D<0`.
   The next target is
   `TypeTwoAffineThresholdCylinderCoverBelowShadowEntry`.
3. **Goldbach.** The exact squared distance from a nonnegative weighted
   reference to an endpoint hole is the sum, over reflection two-cycles, of
   the smaller endpoint square, plus all fixed-point squares. On `Z/4`,
   permutations with every global moment equal can have endpoint
   convolutions `0` and `4s^2`; global moments cannot replace
   orbit-resolved information. The next target is
   `OrbitResolvedVonMangoldtApproximationInsideWeightedHoleRadiusK56`.
4. **Twin Prime.** On the one-variable cubic-rough support, PNT and partial
   summation give prime-to-semiprime ratio `1:log 2` and a negative limiting
   Liouville mean. Identical ambient populations nevertheless admit
   prime-only and semiprime-only selected matchings with opposite deficit
   signs. The next target is
   `PositiveGapTwoCubicRoughMassAndShiftedLogTwoMarginalTransfer`.

한국어 경계: RH 결과는 실제 Weil 상대 작용소를 만들지 않았고, Collatz
임계값은 모든 cylinder에 하강 연장이 있음을 증명하지 않는다. Goldbach
결과는 유한 반사 기하이며 실제 von Mangoldt 오차를 제어하지 않는다.
Twin의 `log 2` 결과는 한 변수 점근식이고 gap-two shifted 상관 하한이
아니다. 네 추측은 모두 `open_not_proven`이고 해결 카운터는 0이다.

## TICKET-152 continuation: compression exhaustion, cylinders, energy, and selection

TICKET-152 tests the four TICKET-151 next lemmas before investing in larger
searches. Three targets require correction.

1. **Riemann Hypothesis.** Nested finite-dimensional compression minima
   decrease to the full spectral infimum. Every finite cutoff can hide a
   new eigenvalue below `-1`, while a finite-rank spectral margin combined
   with a smaller operator-norm tail does certify the full lower bound.
   The next target is
   `ActualWeilCoreCompressionWithCertifiedOperatorNormTailBelowMargin`.
2. **Collatz.** A finite valuation word is one exact residue class modulo
   `2^(S+1)`, and its time-`m` descent set is a terminal arithmetic tail.
   Every possible next valuation occurs inside every cylinder. Consequently
   no finite family of strict word extensions can cover a nonterminal
   cylinder. The next target is
   `TypeTwoCountableExtensionCoverWithUniformAnalyticValuationTail`.
3. **Goldbach.** For a constant baseline, the exact endpoint-hole radius
   squared is `N/2`, whereas the global von Mangoldt error energy is
   asymptotic to `N log N`. The same mismatch holds for uniformly bounded
   dense baselines. The global `L2` bridge is therefore retired. The next
   target is
   `EndpointBilinearVonMangoldtErrorBelowSingularSeriesMainTermK56`.
4. **Twin Prime.** An ambient sign sum `A<0` survives every deletion of
   `q` entries exactly when `q<-A`. The cubic-rough `log 2` limit would
   require about `81.87%` retention, but gap-two rough coverage tends to
   zero by standard sieve orders. The next target is
   `DirectShiftedCubicRoughLiouvilleSumNegativeProportion`.

한국어 경계: RH의 압축 정리는 실제 Weil tail bound가 아니며, Collatz
정리는 countable valuation tail을 제어하지 않는다. Goldbach 정리는
전역 norm 경로를 폐기했을 뿐 endpoint convolution을 하한하지 않고,
Twin 정리는 주변 편향의 이전을 폐기했을 뿐 실제 shifted Liouville
합의 부호를 증명하지 않는다. 네 추측은 모두 `open_not_proven`이며
완전한 증명이나 반례는 없다.

Full bilingual report / 전체 한영 보고서:
[TICKET-152 compression-cylinder-energy-selection](compression-cylinder-energy-selection.md).

## TICKET-153 continuation: essential tails, geometric cylinders, reflection energy, and cubic-rough parity

TICKET-153 attacks the four TICKET-152 next lemmas and closes one exact
subcomponent in each route without changing any conjecture-resolution
counter.

1. **Riemann Hypothesis.** A nonzero positive infinite-dimensional tail
   cannot be approximated by finite-rank operators with norm error below its
   essential size. The correct abstract certificate retains a coercive tail
   `D>=delta I` and pays the coupling cost through
   `A-C*D^(-1)C>=0`. The next target is
   `ActualWeilPositiveTailDecompositionWithCertifiedSchurComplement`.
2. **Collatz.** Every valuation cylinder has the exact countable child law
   `P(a_next=b)=2^-b` and tail `P(a_next>B)=2^-B`. Finite-word linear
   multipliers have negative expected log and an exact negative-binomial
   upper tail. This measure statement does not control affine offsets or
   every natural ray. The next target is
   `UniformAffineOffsetControlOnNaturalValuationRays`.
3. **Goldbach.** For the prime-only theta vector, the endpoint coefficient
   is exactly `||P+ theta||^2-||P- theta||^2`, and it is positive exactly
   when the endpoint has a prime-pair representation. Every symmetric
   baseline leaves `P- theta` unchanged. The next target is
   `ExplicitBinaryPrimeThetaMinorArcBoundBelowMajorArcReflectionGap`.
4. **Twin Prime.** On cubic-rough gap-two support, every endpoint is prime
   or semiprime and the symmetrized shifted Liouville sum is exactly
   `2(QQ-PP)`. Finite checks through 10M have `PP>QQ`, but the next target
   remains the unbounded statement
   `UnboundedCubicRoughPrimePrimeExcessOverSemiprimePairs`.

한국어 경계: RH 정리는 실제 Weil block을 구성하지 않는다. Collatz
정리는 정확한 측도 법칙이지만 모든 자연수 affine threshold를 통제하지
않는다. Goldbach 항등식은 endpoint 양성의 재표현이지 모든 짝수의
하계가 아니다. Twin 항등식은 parity 장벽을 정확히 드러내지만 10M
유한 부호를 무한 scale로 승격하지 않는다. 네 추측은 모두
`open_not_proven`이며 완전한 증명이나 반례는 없다.

Full bilingual report / 전체 한영 보고서:
[TICKET-153 essential-tail-geometric-reflection-parity](essential-tail-geometric-reflection-parity.md).

## TICKET-154 continuation: compact tails, reverse-suffix descent, wheel projection, and least-factor deficit

TICKET-154 attacks the four TICKET-153 next lemmas and closes one exact
subcomponent in each route without changing any conjecture-resolution
counter.

1. **Riemann Hypothesis.** For a finite core, the preconditioned coupling
   `K=D^(-1/2)C` is compact, and a finite Schur margin promotes to the full
   operator when it pays the exact omitted cost
   `||(I-Q_N)K||^2`. A rank-one hidden-direction family refutes every
   uncertified isolated cutoff. The next target is
   `ActualWeilCompactCouplingWithEffectivePreconditionedTailRate`.
2. **Collatz.** If every reverse suffix of a valuation word has average
   valuation at least two, its affine threshold is at most one and every
   odd start above one realizing that word strictly descends. The exact
   geometric mass of length-`m` certificate words is
   `binom(2m,m)/4^m`, so universal occurrence remains open. The next target
   is
   `EveryNaturalValuationRayHitsAReverseSuffixSurplusDescentBlock`.
3. **Goldbach.** Orthogonal projection onto a reflection-symmetric wheel
   space gives an exact sufficient energy certificate. For each fixed
   modulus its energy fraction tends to zero by PNT in arithmetic
   progressions, so fixed-wheel domination is retired. The next target is
   `EffectiveGrowingWheelProjectionDominanceAtEveryLargeEvenEndpoint`.
4. **Twin Prime.** On cubic-rough gap-two support,
   `PP-QQ=R-M`, where `M` counts medium least-prime-factor incidences.
   Small-prime divisibility fingerprints are identical on explicit PP and
   QQ pairs. The next target is
   `UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne`.

한국어 경계: RH 정리는 actual Weil operator를 구성하지 않는다.
Collatz의 reverse-suffix block은 정확한 충분조건이지만 모든 자연수
ray에서의 발생 정리가 없다. Goldbach의 fixed-wheel no-go는 growing
major-arc dominance를 증명하지 않는다. Twin의 incidence 항등식은
`M/R<1`을 무한 scale에서 증명하지 않는다. 네 추측은 모두
`open_not_proven`이며 완전한 증명이나 반례는 없다.

Full bilingual report / 전체 한영 보고서:
[TICKET-154 compact-suffix-wheel-leastfactor](compact-suffix-wheel-leastfactor.md).

## TICKET-155 continuation: range exactness, initial-prefix descent, sublinear wheels, and conditional transfer

TICKET-155 audits the four TICKET-154 next lemmas. It closes four exact
subcomponents, rejects four insufficient bridges, and leaves every
conjecture-resolution counter at zero.

1. **Riemann Hypothesis.** A coupling from a finite-dimensional core has
   finite-dimensional range, and projection onto that range makes the
   omitted coupling tail exactly zero. However, a rank-one vector can have
   any prescribed convergent coordinate-tail profile, so compactness and
   basis coefficients supply no canonical arithmetic convergence rate. The
   next target is
   `ActualWeilFiniteCoreRangeConstructionAndPositiveSchurMatrix`.
2. **Collatz.** The reverse-suffix floor-two condition is exactly the record
   condition `B_m=max_{0<=j<=m} B_j` for the initial prefix surplus walk.
   Every odd start eventually has a one-step local descent, but the infinite
   family `n=4u-1`, `u=3 mod 4`, proves that the resulting endpoint can
   remain above the original start. This corrects the TICKET-154
   occurrence-to-strong-induction bridge. The next target is
   `EveryNaturalStartCrossesAnInitialAffineDescentThreshold`.
3. **Goldbach.** For every fixed `epsilon>0`, a wheel schedule satisfying
   `W_N<=N^(1-epsilon)` captures a vanishing fraction of prime-theta energy.
   Thus neither a fixed wheel nor a fixed-power sublinear growing wheel can
   close the previous projection-energy certificate. The next target is
   `EffectiveGoldbachMajorMinorArcReflectionLowerBoundWithFiniteJoin`.
4. **Twin Prime.** The medium-least-factor incidence ratio is exactly the
   sum of two ambient semiprime densities and two covariance terms divided
   by their partner-event probabilities. A finite probability family has
   covariance tending to zero but a fixed conditional shift, proving that
   unnormalized decorrelation is insufficient under rare conditioning. The
   next target is
   `ShiftTwoCubicRoughSemiprimeRelativeCovarianceSaving`.

한국어 경계: 리만 가설 정리는 actual Weil finite core나 Schur matrix의
양성을 구성하지 않는다. 콜라츠 정리는 기존 귀납 연결을 정정하지만
모든 시작값이 자기 시작값 아래로 내려감을 증명하지 않는다. 골드바흐
정리는 sublinear wheel 경로의 한계를 증명할 뿐 binary minor arc
하계를 주지 않는다. 쌍둥이 소수 정리는 필요한 정규화가 무엇인지
밝히지만 그 상대 covariance 절약을 증명하지 않는다. 네 추측은 모두
`open_not_proven`이며 완전한 증명이나 반례는 없다.

Full bilingual report / 전체 한영 보고서:
[TICKET-155 range-prefix-sublinear-conditional](range-prefix-sublinear-conditional.md).

## TICKET-156 continuation: cutoff, weighted potential, signed loss, and normalized information

TICKET-156 audits the four TICKET-155 next lemmas. It does not close those
infinite lemmas. Instead it proves a sharper bridge or no-go theorem in each
track and identifies the remaining uniform estimate.

1. **Riemann Hypothesis.** Weyl perturbation separates basis/core,
   archimedean-cutoff, and rounding errors. Exact scalar counterfamilies
   show that fixed-cutoff precision stability can have the sign opposite to
   the cutoff-free limit. The next target is
   `ExplicitWeilGalerkinCoreAndUniformTwoAxisOperatorErrorBound`.
2. **Collatz.** The weighted reverse-suffix potential equals `C/2^S`
   exactly and gives the exact affine threshold. The realized valuation
   word `(1,1,2,3)` sends `7` to `5` while violating floor two, so the old
   sufficient rule is not necessary. The next target is
   `EveryNaturalValuationRayCrossesItsWeightedSuffixPotential`.
3. **Goldbach.** The inverse DFT gives the one-sided certificate
   `R_2(N)>=M_N-N_N^-`, which charges only harmful negative minor phase
   mass. It is sharper than the phase-blind Parseval budget, but a fixed
   `q<=8` mask still fails on the last three of six audited endpoints. The
   next target is
   `UniformBinaryGoldbachMinorNegativePhaseMassBoundWithFiniteJoin`.
4. **Twin Prime.** Pinsker gives `I(D;B)>=2 rho delta^2`; therefore rare
   transfer requires `I=o(rho)`. An exact family has `I->0` but fixed
   `delta=1/5`, disproving unnormalized information transfer. The next
   target is
   `ShiftTwoCubicRoughMutualInformationLittleOSelectionMass`.

한국어 경계: RH의 실제 Weil 행렬과 균일 cutoff bound는 아직 없다.
콜라츠의 weighted potential 항등식은 주어진 prefix를 판정할 뿐 모든
자연수 ray의 first passage를 증명하지 않는다. 골드바흐의 음의 위상
질량은 유한 DFT에서 계산되었고 균일한 해석적 상계가 아니다. Twin의
Pinsker 정리는 충분조건을 제시하지만 실제 cubic-rough shift에서
`I=o(rho)`를 증명하지 않는다. 네 추측은 모두 `open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-156 cutoff-potential-signed-information](cutoff-potential-signed-information.md).

## TICKET-157 continuation: form cores, inversion gain, phase proxies, and information margins

TICKET-157 attacks the four TICKET-156 next lemmas. It proves four exact
reductions or no-go theorems, rejects one overstrong or dimension-blind
target per track, and leaves every conjecture-resolution counter at zero.

1. **Riemann Hypothesis.** Positivity on every member of a nested form core
   plus one uniform cutoff-form error promotes to the full closed form.
   Exact diagonal countermodels show that no finite core sweep suffices.
   The actual Weil core and its tail bound remain open. The next target is
   `UniformArchimedeanTailFormBoundOnNestedExplicitWeilCore`.
2. **Collatz.** Adjacent valuation swaps telescope to an exact affine
   inversion gain. The descent condition is exactly that this gain exceeds
   the descending worst-order threshold excess. Of 49,999 audited first
   descents, 266 require natural order. The next target is
   `NaturalValuationInversionGainDominatesWorstOrderThresholdExcess`.
3. **Goldbach.** Negative minor phase mass is one-Lipschitz in complex
   `L1`. An exact constant-residual family proves that converting an `L2`
   proxy error costs a sharp square-root dimension factor. All 18
   target-fitted block proxies fail. The next target is
   `ArithmeticBinaryGoldbachPhaseProxyWithUniformL1ResidualAndFiniteJoin`.
4. **Twin Prime.** Combining the exact conditional-transfer identity with
   Pinsker gives an information upper bound for `M/R`; all five finite
   scales through 10M lie below one. A rare-event family proves
   `I=o(rho)` is sufficient but not necessary. The next target is
   `UniformCubicRoughInformationBudgetBelowSemiprimeMarginAfterEffectiveCutoff`.

한국어 경계: RH 결과는 actual Weil tail-form bound를 제공하지 않는다.
Collatz inversion gain은 선택한 prefix의 하강을 다시 표현할 뿐 모든
자연수 ray의 gain 하한을 증명하지 않는다. Goldbach block proxy는
target-fitted 진단이며 analytic major-arc 모형이 아니다. Twin의 다섯
정보량 인증은 유한 결과이고 uniform post-cutoff 정리가 아니다. 네
추측은 모두 `open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-157 formcore-inversion-proxy-margin](formcore-inversion-proxy-margin.md).

## TICKET-158 continuation: two cutoffs, localized gain, phase variation, and directional information

TICKET-158 attacks the four TICKET-157 open lemmas. It incorporates a new
fixed-`(c,N)` archimedean-tail literature boundary without claiming that
external theorem as a PrimeProject result, and proves four new exact
composition or no-go statements.

1. **Riemann Hypothesis.** A positive archimedean tail and an absolute
   prime/band remainder compose into exact positive and negative form
   certificates. A scalar family proves that sending only the archimedean
   tail to zero cannot control the full form. The next target is
   `UniformPrimeBandRemainderOnExplicitNestedWeilCoreWithJointCutoffSchedule`.
2. **Collatz.** The words `(K,1,1,1,2)` and `(2,1,1,K,1)` have the same
   length, valuation sum, multiset, and ordinary inversion count but
   different exact affine gains for every `K>=6`. The next target is
   `NaturalValuationPrefixLocalizedGainCrossesAffineThresholdOnEveryRay`.
3. **Goldbach.** A cyclic width-`b` moving average obeys the sharp bound
   `||w-A_b w||_1 <= (b-1)TV(w)/2`. Alternating signs saturate it and all
   18 raw finite variation certificates fail. The next target is
   `ArithmeticMinorArcPhaseVariationBelowMajorMarginWithEffectiveFiniteJoin`.
4. **Twin Prime.** The target upper bound needs information budget only on
   positive conditional shifts. Four of five finite rows improve strictly,
   but symmetric Bernoulli tables show that mutual information cannot
   determine the shift sign. The next target is
   `UniformPositiveCubicRoughInformationBudgetOrSemiprimeAnticorrelationAfterEffectiveCutoff`.

한국어 경계: RH의 새 문헌은 고정 `(c,N)` archimedean tail을 다루지만
prime/band joint limit를 증명하지 않는다. Collatz 반례군은 affine
valuation word에 대한 no-go이며 발산 orbit이 아니다. Goldbach
variation 값은 유한 DFT 관측이고 균일 산술 상계가 아니다. Twin의
shift 부호는 유한 데이터에서 계산되었지만 mutual information만으로
전칭 승격할 수 없다. 네 추측은 모두 `open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-158 two-cutoff-localized-variation-directional](two-cutoff-localized-variation-directional.md).

## TICKET-159 continuation: diagonal selectors, affine thresholds, Fourier phase, and parity

TICKET-159 attacks the four TICKET-158 open lemmas. It proves four exact
reductions or no-go theorems, removes one unnecessary or information-losing
condition per track, and keeps every conjecture-resolution counter at zero.

1. **Riemann Hypothesis.** Computable monotone prime/band and tail
   majorants can be searched separately for every nested core by a finite
   doubling selector. An adversarial family proves that pointwise
   convergence supplies no preassigned cutoff schedule. The next target is
   `CertifiedPrimeBandMajorantAndPositiveGalerkinMarginOnEveryNestedWeilCore`.
2. **Collatz.** A valuation prefix descends exactly when
   `(2^S-3^m)n>C(w)`. Minimal positive log contraction has unbounded affine
   thresholds along an irrational-rotation subsequence, so average
   contraction alone is insufficient. The next target is
   `EveryNaturalOddOrbitHasARealizedPrefixAboveItsExactAffineThreshold`.
3. **Goldbach.** The signed minor coefficient is bounded by minor `L2`
   energy, but equal-energy Hermitian spectra can have opposite target
   coefficient signs. All eight finite energy-only audits fail to certify.
   The next target is
   `PhaseSensitiveBilinearMinorArcCoefficientBelowExplicitSingularSeriesMargin`.
4. **Twin Prime.** Low-prime divisibility bits are constant on a rough
   fiber and therefore have exactly zero conditional mutual information.
   All ten finite fibers contain twin and double-composite witnesses. The
   next target is
   `NonlocalTypeIIOrParitySensitiveCorrelationSeparatesPrimePairsFromRoughCompositePairsUniformly`.

한국어 경계: RH의 selector는 실제 Weil 오차 상계와 양의 finite-core
margin을 증명하지 않는다. Collatz threshold 정리는 자연 orbit마다
threshold crossing이 존재함을 증명하지 않는다. Goldbach energy
상계는 위상을 버리므로 uniform signed coefficient 정리가 아니다.
Twin rough-fiber no-go는 저소수 divisibility sigma algebra에만
적용되며 Type II 상관을 배제하지 않는다. 네 추측은 모두
`open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-159 diagonal-threshold-phase-parity](diagonal-threshold-phase-parity.md).

## TICKET-160 continuation: exact support, natural cylinders, bilinear phase, and wheel limits

TICKET-160 audits and corrects the four TICKET-159 next targets. It proves four
exact theorem/no-go packages, records one stricter next lemma per track, and
keeps all conjecture-resolution counters at zero.

1. **Riemann Hypothesis.** In the finite Guinand-Weil dictionary, every
   prime power above cutoff `c` has exactly zero Fourier weight. Raw
   zero-extended Galerkin spaces at distinct cutoffs have zero intersection,
   so they cannot be treated as nested compressions. The next target is
   `EffectiveCommonNestedWeilCoreTransport`.
2. **Collatz.** Every finite valuation word has one exact odd residue
   cylinder, and contracting cylinders have cofinite descending tails. The
   infinite family `w_m=(m+1,1,...,1)` has thresholds tending to infinity,
   yet every natural realizer descends. The next target is
   `MinimalContractingFrontLoadedNaturalTransfer`.
3. **Goldbach.** The minor proxy defect is an exact reflection bilinear form
   with no explicit square-root dimension loss. Centered cosine and sine
   modes saturate the Cauchy bound with signs `+1` and `-1`, proving that
   arithmetic input is necessary. The next target is
   `PrimeRestrictedMinorProxyDefectBelowExplicitSingularSeriesMargin`.
4. **Twin Prime.** CRT creates double-composite mimics in every fixed wheel
   residue. On cubic-rough finite ranges, proper-factor features separate PP
   from QQ exactly when their search depth reaches the factor horizon
   `tau_X`; at `X=10M`, `tau_X=3037`. The next target is
   `IndependentCubicRoughBilinearIncidenceDeficit`.

한국어 경계: RH 결과는 common Weil core나 양의 margin을 만들지 않는다.
Collatz의 무한 가족 정리는 선택한 front-loaded 가족만 닫으며 모든
orbit을 다루지 않는다. Goldbach의 sharp 반례는 일반 실수 수열이고
prime DFT 반례가 아니다. Twin의 factor horizon은 유한 trial-division
복잡도를 측정하며 Type II 하계를 제공하지 않는다. 네 추측은 모두
`open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-160 exact-support-cylinder-bilinear-wheel](exact-support-cylinder-bilinear-wheel.md).

## TICKET-161 continuation: common-core resolution, Baker reduction, reflection angles, and Type II incidence

TICKET-161 attacks the four TICKET-160 open lemmas. It closes one exact
intermediate theorem or no-go statement per track, records the remaining
uniformity gap, and keeps all conjecture-resolution counters at zero.

1. **Riemann Hypothesis.** For zero-extended
   `f in H^1_0(-a,a)`, Fourier projection on `(-L,L)` satisfies
   `||f-P_(L,N)f||_2 <= L||f'||_2/(pi(N+1))`. Thus a fixed compact
   finite-dimensional core has effective common `L2` transport when
   `N/L -> infinity`. The tent function proves bounded `N/L` is insufficient.
   The next target is
   `UniformWeilFormGraphNormTransportOnResolvedCommonCore`.
2. **Collatz.** For the minimal front-loaded word
   `w_m=(ceil(m log_2 3)-m+1,1,...,1)`, failed natural descent forces the
   reduced fraction `ceil(m log_2 3)/m` to be a continued-fraction convergent.
   A Baker-Wüstholz linear-form lower bound eventually dominates the
   exponentially small failure window, proving eventual descent for this one
   family. The scan through `m=50,000` finds no finite exception. The next
   target is
   `ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily`.
3. **Goldbach.** A symmetric minor projection gives the exact identity
   `G_f(N)=M(N)+rho_N||P_minor f||_2^2`. The harmful targetwise angle therefore
   strictly refines phase-blind Cauchy control. A two-point spike proves that
   vanishing mean or RMS angle does not imply a uniform targetwise bound. The
   next target is
   `UniformPrimeMinorReflectionAngleBelowMajorArcMargin`.
4. **Twin Prime.** A `2x2` zero-marginal checkerboard is invisible to all
   separate row and column marginals but has nonzero bilinear correlation.
   Centered cubic-rough least-factor incidence therefore measures a genuine
   finite Type-II dependence component; its decreasing ratios through 10M are
   observations, not an asymptotic theorem. The next target is
   `UniformCubicRoughCenteredIncidenceSpectralDecay`.

한국어 경계: RH의 `L2` 수송은 Weil form norm이나 양의 margin을 주지
않는다. Collatz의 점근 정리는 명시한 한 valuation 가족만 다루며 전체
궤도를 덮지 않는다. Goldbach의 finite angle은 실제 prime DFT에서
계산한 진단값이므로 독립적인 minor-arc 증명이 아니다. Twin의 유한
spectral 감소는 균일 Type-II 하계나 양의 twin-prime 하계를 주지
않는다. 네 추측은 모두 `open_not_proven`이다.

Full bilingual report / 전체 한영 보고서:
[TICKET-161 commoncore-baker-angle-typeii](commoncore-baker-angle-typeii.md).

## TICKET-171 continuation: relative KKT geometry, a 2-adic ghost ray, signed phase, and Haar resolution

TICKET-171 audits the latest four open lemmas rather than extending finite
cutoffs. It proves four exact target corrections and keeps every conjecture
resolution counter at zero.

1. **Riemann Hypothesis.** The sign-normalized relative error
   `F=|K|^(-1/2)E|K|^(-1/2)` preserves KKT inertia when `||F||_2<1`.
   An anisotropic family proves that the global minimum gap is not a necessary
   absolute error scale. The next target is
   `CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore`.
2. **Collatz.** The full residual child tree is not well founded. The all-one
   words have least realizers `2^(m+1)-1`, remain non-descending, and converge
   to the non-natural 2-adic start `-1`. The corrected next target is
   `NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay`.
3. **Goldbach.** Two nonnegative squared signals on `Z/4` have identical
   Fourier magnitudes and shell energies but maxima `1+2e` and `1+e`.
   Shell-energy-only sharp certification is rejected. The next target is
   `UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin`.
4. **Twin Prime.** A two-dimensional orthogonal Haar transform preserves the
   full Type-II operator and Frobenius energy. Every fixed maximum depth misses
   a next-scale checkerboard with singular value `2a`. The next target is
   `UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants`.

한국어 경계: 상대 KKT 정리는 실제 Weil core의 cofinal 구간 상계를 만들지
않는다. 콜라츠 all-one 경로는 양의 자연수 발산 궤도가 아니라 2-adic 유령
경로다. 골드바흐 위상 반례는 일반 비음수 신호이며 소수 특화 반례가 아니다.
Twin Haar 항등식은 좌표 변환일 뿐 점근 Type-II decay를 제공하지 않는다.
네 추측은 모두 `open_not_proven`이다.

English report: [TICKET-171 relative-ghost-phase-haar](relative-ghost-phase-haar.md).
한국어 보고서: [TICKET-171 상대-유령-위상-Haar](relative-ghost-phase-haar.ko.md).

## TICKET-172 continuation: structured blocks, bridge equivalence, Fourier L1, and mixed variation

TICKET-172 audits the latest four terminal nodes and proves four exact
intermediate statements without resolving a conjecture:

1. RH: saddle-point congruence reduces KKT inertia to primal positivity and
   constraint full row rank. A 2x2 family refutes necessity of a whole relative
   KKT norm below one. The next target is
   `CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate`.
2. Collatz: exclusion of every positive-natural non-descending residual ray is
   equivalent to Collatz first descent. The route is rejected as a weaker
   bridge. The next target is `LeastCounterexampleCrossScaleCylinderHeightBound`.
3. Goldbach: Fourier inversion gives the exact pointwise L1 positivity gate,
   and the positive Z/4 family saturates it with unchanged magnitudes. The next
   target is `UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm`.
4. Twin Prime: fine/fine Haar energy equals one quarter of the dyadic mixed
   difference square sum. Checkerboards refute marginal-only control. The next
   target is `PrimePairMatrixWeightedDyadicMixedVariationPowerSaving`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-172 structure-equivalence-l1-variation](structure-equivalence-l1-variation.md).
한국어 보고서: [TICKET-172 구조-동치-L1-혼합변동](structure-equivalence-l1-variation.ko.md).

## TICKET-173 continuation: finite sections, cylinder stabilization, target phase, and tensor-Haar pairs

TICKET-173 proves four exact limiting-coordinate statements and keeps every
conjecture resolution counter at zero:

1. RH: nested dense finite sections with lower defect `eta_N->0` imply global
   nonnegativity. `diag(1/j)` refutes necessity of a uniform positive gap. The
   next target is `PoleNeutralWeilFiniteSectionLowerDefectConvergesToZero`.
2. Collatz: every valuation word has one odd cylinder representative modulo
   `2^(S+1)`, and positive-natural support is equivalent to eventual
   stabilization. All-one prefixes reject horizon-only subexponential height.
   The next target is
   `EveryPrefixwiseNonDescendingRayHasUnboundedCylinderRepresentatives`.
3. Goldbach: target-aligned inversion gives `R(n)=anchor+P(n)-N(n)`. A
   nonnegative weighted Z/8 signal has positive convolution although
   `N(n)>anchor`, rejecting necessity of the negative-only gate. The next
   target is `UniformMajorArcPositiveMassDominatesMinorArcSignedDeficit`.
4. Twin Prime: complete Type-II Haar energy uses independent row and column
   scale indices. Unequal-scale rank-one wavelets have zero same-scale energy
   and norm one. The corrected target is
   `PrimePairMatrixAllScalePairHaarEnergyPowerSaving`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-173 finite-section-cylinder-phase-tensor](finite-section-cylinder-phase-tensor.md).
한국어 보고서: [TICKET-173 유한단면-cylinder-위상-tensor](finite-section-cylinder-phase-tensor.ko.md).

## TICKET-174 continuation: tail schedules, unique zero lifts, adaptive selection, and scale aggregation

TICKET-174 proves four exact quantitative statements while keeping every
conjecture resolution counter at zero:

1. RH: if the truncated arithmetic defect plus the known archimedean tail
   tends to zero on one diagonal schedule, dense-core nonnegativity follows.
   The explicit certified tail upper bound vanishes for `T_N=N^2`, while
   linear or critical `N log N` schedules do not certify closure through that
   bound. The next target is
   `PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero`.
2. Collatz: every finite valuation cylinder has exactly one zero-lift child.
   Its truncated local density is at most `1/A`, yet every stabilized natural
   ray follows that exceptional child forever. The next target is
   `NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren`.
3. Goldbach: a target-dependent set of positive Fourier terms selected after
   observing the aligned signs exists exactly when the representation count is
   positive. This post-hoc route is circular. The next target is
   `FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly`.
4. Twin Prime: all tensor-Haar scale-pair energies aggregate with a sharp
   `log2 N` loss from their maximum to the operator norm. The next target is
   `PrimePairEveryScalePairHaarEnergyPowerSavingUniformly`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-174 tail-lift-adaptive-scalepair](tail-lift-adaptive-scalepair.md).
한국어 보고서: [TICKET-174 tail-lift-adaptive-scalepair](tail-lift-adaptive-scalepair.ko.md).

## TICKET-175 continuation: relative resolution, equivalence correction, signed minors, and block operators

TICKET-175 proves four exact reductions while keeping every conjecture
resolution counter at zero:

1. RH: Weyl perturbation makes an absolute positivity certificate require a
   rigorous finite margin above the tail norm. The explicit polynomial-cutoff
   tail bound cannot resolve a superpolynomially small spectral edge. Published
   Galerkin branch magnitudes are used only as numerical resolution targets.
   The next target is
   `StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale`.
2. Collatz: eventual non-descent along unique zero-lift children is equivalent
   to coefficient stopping and therefore to Collatz. This target is rejected
   as a weaker intermediate lemma. The next target isolates aperiodic rays:
   `EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary`.
3. Goldbach: for a fixed Fourier major mask, the absolute-minor certificate
   margin is exactly `R-2 P_minor`. An L1 replacement loses every positive
   minor term twice. The next target is
   `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly`.
4. Twin Prime: with Haar scale blocks `A_jk` and scalar matrix
   `B_jk=||A_jk||_op`, the exact domination `||A||_op<=||B||_op` can recover
   the logarithmic max-energy loss. The next target is
   `PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-175 relative-equivalence-signed-block](relative-equivalence-signed-block.md).
한국어 보고서: [TICKET-175 relative-equivalence-signed-block](relative-equivalence-signed-block.ko.md).

## TICKET-176 continuation: relative cones, harmonic corrections, parity aliases, and weighted Schur circularity

TICKET-176 proves four exact reductions and keeps all conjecture-resolution
counters at zero:

1. RH: `A_T>=delta G` and a two-sided relative tail bound imply
   `A>=(delta-epsilon)G`. A 2-by-2 countermodel proves diagonal tail data cannot
   replace the full form inequality. The next target is
   `PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin`.
2. Collatz: distinct odd states on an aperiodic non-descending prefix bound the
   exact affine correction by an explicit `O(log h)` harmonic envelope. Start
   63 refutes treating envelope crossing as an iff descent criterion, while
   `2^m-1` refutes every fixed descent horizon. The next target is
   `AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope`.
3. Goldbach: frequencies `k` and `k+L/2` have identical phases on all even
   targets, giving a lossless parity quotient before absolute values. The
   finite Q=16 count improves from 367 to 377, but the next target remains the
   arithmetic uniform theorem
   `ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain`.
4. Twin Prime: the infimum of the weighted-Schur bound over unrestricted
   positive weights equals the block spectral norm. Therefore fitted weights
   are circular; the next target is
   `PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-176 relative-cone-harmonic-alias-schur](relative-cone-harmonic-alias-schur.md).
한국어 보고서: [TICKET-176 relative-cone-harmonic-alias-schur](relative-cone-harmonic-alias-schur.ko.md).

## TICKET-228 continuation: near aliases, affine languages, and residue spectra

TICKET-228 directly tests the four open lemmas from TICKET-227. It proves four
exact partial or no-go theorems and keeps the conjecture-resolution count at
zero:

1. RH: every finite dilation family has arbitrarily large simultaneous near
   aliases by simultaneous Dirichlet approximation. This refutes a positive
   full-line uniform frame bound. The corrected target is a bandlimited
   Weil-core estimate with explicit Diophantine loss.
2. Collatz: the equal-slope blocks `(1,3,3,1)` and `(2,3,1,2)`, followed by
   `(1,4,1)`, produce `2^r` distinct primitive noncycles at every depth `r`,
   all with `887/700 <= B/D <= 7123/5600`. A cofinal cover and aperiodic
   descent remain open.
3. Goldbach: the unit-residue mask `M_a` has an exact target-dependent
   singular spectrum. For nonzero `a`, the nonconstant modes all survive with
   singular value `1`; scalar local density therefore cannot replace uniform
   moving-target character cancellation.
4. Twin Prime: the `qr-2` and `qr+2` masks have exact cross Gram operator
   `(l-3)J+P_2P_{-2}`. Their simultaneous local-survival route is impossible
   modulo `3`; separate uniform shift-two character cancellation remains open.

Machine audit: four exact partial theorems, four rejected or narrowed routes,
four proof DAGs, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-228 near aliases, affine languages, and residue spectra](near-alias-affine-language-residue-spectrum.md).
한국어 보고서: [TICKET-228 근접 에일리어스·아핀 언어·잉여류 스펙트럼](near-alias-affine-language-residue-spectrum.ko.md).

## TICKET-227 preserved continuation: Mellin, block, and Buchstab factor lifts

TICKET-227 continues the TICKET-226 proof DAG and proves four exact structural
lemmas while keeping the conjecture-resolution count at zero:

1. RH: a single dilation ratio has infinitely many Mellin aliases, while
   ratios `2` and `3` have no common nonconstant alias on `Re(s)=1`. The next
   target is `UniformDualDilationMellinFrameBoundOnExplicitDenseWeilCore`.
2. Collatz: a fractional-linear endpoint theorem proves every
   `(1,1,3)^r,(4,2,1)` is a primitive noncycle with `1<B/D<2`. The next target
   is `UniversalPrimePowerWitnessForPrimitiveValuationWordNondivisibility`.
3. Goldbach: the cube-root `PS`, `SP`, and `SS` channels lift exactly to
   factor-resolved moving-residue cells, including a one-candidate split when
   `q|N`. The next target is
   `UniformMovingResiduePrimeEstimateForCubeRootBuchstabCellsAtEveryEvenTarget`.
4. Twin Prime: the shifted channels lift exactly to `qr-2`, `qr+2`, and
   `pq+2=rs`; every `SS` factor graph is disjoint. The next target is
   `UniformShiftTwoBilinearPrimeEstimateForQrPlusMinus2AcrossAllCubeRootCells`.

Machine audit: four exact structural lemmas, four rejected or corrected
routes, four proof DAGs, zero conjecture resolutions, and zero computational
failures.

English report: [TICKET-227 Mellin, block, and Buchstab factor lifts](mellin-block-buchstab-lifts.md).
한국어 보고서: [TICKET-227 Mellin·반복 블록·Buchstab 인수 분해](mellin-block-buchstab-lifts.ko.md).

## TICKET-226 preserved continuation: signal transfer and same-order obstructions

TICKET-226 continues the TICKET-225 proof DAG and proves four exact transfer
or no-go statements while keeping the conjecture-resolution count at zero:

1. RH: the actual prime Laplace band is exactly a Chebyshev-error integral
   against a balanced sign-changing kernel with negative and positive masses
   `-1/4` and `+1/4`. A band sign is therefore not direct Weil positivity. The
   next target is
   `ExplicitFormulaControlOfBalancedChebyshevBandsOnDenseWeilCore`.
2. Collatz: every word `(1,1,3)^r,2` is primitive and noncyclic, yet all its
   cyclic intercepts exceed `D`. This infinite family rejects universal
   minimum-intercept descent; the next target is
   `NoNontrivialPrimitiveValuationWordSatisfiesDDividesB`.
3. Goldbach: cube-root rough semiprimes satisfy
   `S_z(X)~(log 2)X/log X`, the same marginal order as primes. Exact finite
   rows also refute total contamination below `PP`; the next target is
   `FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly`.
4. Twin Prime: Type-I rough-semiprime marginals are likewise same-order and
   cannot yield shifted pair separation. Exact finite rows reject
   contamination below `PP` at two larger horizons; the next target is
   `ShiftedCubeRootParityTypeIIBilinearPowerSavingOnUnboundedBlocks`.

Machine audit: four exact transfer or no-go theorems, four rejected or
corrected routes, four proof DAGs, zero conjecture resolutions, and zero
computational failures.

English report: [TICKET-226 signal transfer and same-order obstructions](signal-transfer-same-order-obstructions.md).
한국어 보고서: [TICKET-226 신호 전달과 같은 차수 방해항](signal-transfer-same-order-obstructions.ko.md).

## TICKET-225 preserved continuation: arithmetic remainder localization

TICKET-225 continues the TICKET-224 proof DAG and proves four exact arithmetic
localization or no-go statements while keeping the conjecture-resolution count
at zero:

1. RH: the actual von Mangoldt Laplace-band tail beyond `N` is positive and is
   bounded by `q^(N+1)((N+1)-Nq)/(1-q)^2`. Finite band families remain
   non-injective, so the missing theorem is an explicit-formula transfer from
   cofinal margins to positivity on a dense Weil core.
2. Collatz: cyclic intercepts satisfy `2^a B'=3B+D`, hence their gcd residual
   is rotation-invariant. Rotation-wise deficits are not independent; a
   uniform intercept descent or separate aperiodic-orbit descent remains open.
3. Goldbach: under `z^3>=X`, the wheel indicator is exactly `Q=P+S`, where
   `S` is the rough-semiprime indicator. The three contamination convolutions
   must still be uniformly dominated by the prime-prime main term.
4. Twin Prime: the same classification gives the exact pair split
   `PP+PS+SP+SS`. Explicit SS pairs refute survivor certificates; a positive
   PP lower bound after controlling all contamination remains open.

Machine audit: four exact localization or no-go theorems, four rejected or
corrected routes, four proof DAGs, zero conjecture resolutions, and zero
computational failures.

English report: [TICKET-225 arithmetic remainder localization](arithmetic-remainder-localization.md).
한국어 보고서: [TICKET-225 산술적 나머지 국소화](arithmetic-remainder-localization.ko.md).

## TICKET-224 preserved continuation: sharp completeness thresholds

TICKET-224 continues the TICKET-223 proof DAG and proves four exact threshold
or no-go statements while keeping the conjecture-resolution count at zero:

1. RH: the exponential dyadic-band tail has the optimal uniform constant
   `1/4`, attained by aligned atoms. The missing bridge is a rigorous
   actual-zeta prime-side band margin above this sharp envelope.
2. Collatz: finite-cycle divisibility is equivalent to every prime-power
   valuation inequality. The primitive word `(1,1,2,4,3)` satisfies
   `rad(D)|B` but not `D|B`, refuting radical-only adaptive tests. Universal
   prime-power deficit and aperiodic descent remain open.
3. Goldbach: factor filtering through `sqrt(X)` equals primality on `[2,X]`,
   but every fixed lower cutoff admits semiprime false diagonals. The missing
   theorem is a uniform sub-square-root prime-weighted remainder below the
   positive local margin.
4. Twin Prime: square-root filtering exactly decides bounded gap-two
   candidates, while every lower fixed cutoff admits infinite CRT composite
   progressions. Uniform sub-square-root Type-II separation remains open.

Machine audit: four exact threshold or no-go theorems, four rejected routes,
four proof DAGs, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-224 sharp completeness thresholds](sharp-completeness-thresholds.md).
한국어 보고서: [TICKET-224 날카로운 완전성 임계값](sharp-completeness-thresholds.ko.md).

## TICKET-223 preserved continuation: exponential tails, local duality, and fixed-sieve no-go

TICKET-223 continues the latest proof DAG rather than restarting a classical
reproduction. It proves four exact partial or no-go statements while keeping
the conjecture-resolution count at zero:

1. RH: complete dyadic Laplace data remain injective for signed measures with
   an exponential total-variation moment, and every band has a uniform
   exponentially decaying truncation error. The missing bridge is an
   RH-equivalent actual-zeta defect with rigorous prime-side bands.
2. Collatz: every finite fixed family of `(D,B)` congruence tests whose moduli
   are coprime to six admits a primitive non-cycle false positive. The theorem
   does not exclude code-growing divisibility obstructions or prove descent of
   every aperiodic orbit.
3. Goldbach: the normalized local convolution count on every finite odd wheel
   is bounded below by the positive factor
   `C_W=product p(p-2)/(p-1)^2`. This gives no prime-weighted global remainder
   estimate.
4. Twin Prime: every fixed wheel survivor class contains an infinite CRT
   progression of composite pairs. Its normalized survivor density is exactly
   the Goldbach minimum factor `C_W`, but no scale-growing Type-II lower bound
   follows.

Machine audit: four exact partial theorems, four refuted or corrected routes,
four proof DAGs, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-223 exponential-tail-local-duality-no-go](exponential-tail-local-duality-no-go.md).
한국어 보고서: [TICKET-223 지수 꼬리·국소 쌍대성·고정 체 no-go](exponential-tail-local-duality-no-go.ko.md).

## TICKET-229 continuation: band frames, semilinear coverage, and character barriers

TICKET-229 directly tests the four open lemmas from TICKET-228 and keeps the
parent-conjecture resolution count at zero:

1. RH: `F(tau)=|1-2^(-itau)|^2+|1-3^(-itau)|^2` has an explicit positive
   lower bound on every finite band. The bound decays exponentially, so it
   cannot by itself dominate a merely polynomial Weil-core truncation tail.
2. Collatz: each fixed-suffix equal-slope language lies on one affine `(h,S)`
   line. No finite union is cofinal among primitive positive-denominator
   words; exact cycle nondivisibility and aperiodic descent remain open.
3. Goldbach: averaging one complete target-residue period annihilates every
   nonconstant local character exactly, but each fixed nonzero target is still
   an isometry on that space. Prime-weighted pointwise cancellation remains
   open.
4. Twin Prime: shift-two symmetry annihilates odd characters, while the
   modulo-5 quadratic character has normalized singular ratio one. Local
   tensorization alone cannot remove it; prime-weighted cancellation remains
   open.

Machine audit: four exact partial or no-go theorems, four rejected or narrowed
routes, four proof DAGs, zero conjecture resolutions, and zero computational
failures.

English report: [TICKET-229 band frames, semilinear coverage, and character barriers](band-frame-semilinear-character-barriers.md).
한국어 보고서: [TICKET-229 대역 프레임·준선형 포괄·지표 방해](band-frame-semilinear-character-barriers.ko.md).

## TICKET-231 continuation: summable frames, the Collatz critical strip, a Gauss counterfamily, and CRT orthogonality

TICKET-231 proves four exact partial or no-go results and keeps the
parent-conjecture resolution count at zero:

1. RH: every fixed absolutely summable infinite dilation family has energy
   liminf zero, so the naive infinite-frame repair cannot provide a positive
   uniform floor. A height-adaptive or renormalized frame with explicit
   Weil-tail dominance remains open.
2. Collatz: every nontrivial positive cycle lies in the strict strip
   `log_2(3)<S/h<2`. Critical-strip necklace nondivisibility and aperiodic
   descent remain open.
3. Goldbach: quadratic residues modulo primes `3 mod 4` give a true
   zero-convolution Gauss counterfamily while every relative nonprincipal mode
   tends to zero. This corrects the stronger TICKET-230 wording but does not
   estimate prime weights.
4. Twin Prime: centered quadratic CRT interaction tensors are exactly
   orthogonal with explicit norms. Prime-weighted growing-modulus saving and a
   positive principal lower bound remain open.

Machine audit: four exact partial or no-go theorems, four rejected or corrected
routes, four proof DAGs, zero conjecture resolutions, and zero computational
failures.

English report: [TICKET-231 summable frames, critical strip, Gauss counterfamily, and CRT orthogonality](summable-frame-critical-strip-gauss-crt.md).
한국어 보고서: [TICKET-231 절대가합 프레임·임계띠·가우스 반례족·CRT 직교성](summable-frame-critical-strip-gauss-crt.ko.md).

## TICKET-232 continuation: effective dimension, binary defects, rational shells, and CRT sparsity

TICKET-232 proves four exact partial or no-go theorems and keeps the
parent-conjecture resolution count at zero:

1. RH: every adaptive positive normalized frame floor needs logarithmically
   many effective dilation coordinates. A logarithmically dense frame with
   explicit Weil-tail dominance remains open.
2. Collatz: every positive binary valuation word with one, two, or three
   valuation-one entries is nondivisible. The four-one layer, valuations at
   least three, and aperiodic descent remain open.
3. Goldbach: every actual-prime denominator-prime rational shell has an exact
   target-aligned residue-autocorrelation decomposition. Classwise relative
   equidistribution `o(1)` alone does not control growing-shell size or sign.
4. Twin Prime: full normalized CRT interaction energy equals chi-square and
   obeys a sparse-support lower bound. Only the full unweighted positive
   energy-saving route is refuted; entropy-matched signed Type-II estimates
   and a positive principal lower bound remain open.

Machine audit: four exact partial or no-go theorems, four discarded routes,
four proof DAGs, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-232 effective dimension, binary defects, rational shells, and CRT sparsity](effective-dimension-binary-defect-rational-shell-crt-sparsity.md).
한국어 보고서: [TICKET-232 유효차원·binary defect·유리 shell·CRT 희소성](effective-dimension-binary-defect-rational-shell-crt-sparsity.ko.md).

## TICKET-233 continuation: logarithmic frames, twelve-one Collatz closure, squarefree shells, and CRT entropy

TICKET-233 proves four exact partial, asymptotic, or no-go theorems and keeps
the parent-conjecture resolution count at zero:

1. RH: a scalar adaptive frame with unit floor exists in `O(log T)`
   coordinates, matching TICKET-232's lower bound. Transfer to the signed Weil
   kernel with explicit arithmetic-tail dominance remains open.
2. Collatz: the TICKET-232 four-one successor is corrected as already closed,
   and the first open binary fixed stratum `k=12` is exhaustively excluded by
   an exact `5+6` MITM over the complete finite decision range. Uniform binary
   `k>=13`, larger valuations, and aperiodic descent remain open.
3. Goldbach: odd-squarefree rational shells satisfy an explicit discrepancy
   bound and a prime-weighted asymptotic for polylogarithmic denominators.
   Actual primes refute an uncoupled all-growing-denominator statement.
4. Twin Prime: product-damped centered CRT energy and signed aggregates obey
   exact entropy bounds. Critical damping plus local centering, and bounded
   entropy plus full-parity retention, are refuted in the CRT model.

Machine audit: four exact partial, asymptotic, or no-go theorems, four
discarded/corrected routes, four proof DAGs, one lineage correction, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-233 logarithmic frames, Collatz twelve-one closure, squarefree shells, and CRT entropy](logarithmic-frame-density-shell-entropy.md).
한국어 보고서: [TICKET-233 로그 프레임·Collatz 12-one·squarefree shell·CRT 엔트로피](logarithmic-frame-density-shell-entropy.ko.md).

## TICKET-235 continuation: Schur complements, prime-power deficits, Goldbach phase retrieval, and CRT overlaps

TICKET-235 proves four exact partial or no-go theorems and keeps the
parent-conjecture resolution count at zero:

1. RH: full positivity is equivalent to a relative kernel Schur complement;
   positive kernel compression plus absolute cross-block smallness is not
   enough.
2. Collatz: after restoring the general prime-power witness to TICKET-224, an
   exact run-block order characterization shows that an arbitrary primitive
   divisor can also divide the binary numerator.
3. Goldbach: complete separate marginal Fourier powers can agree while the
   target-reflected cross coefficient changes from two to zero.
4. Twin Prime: fixed-degree CRT Cesaro energies are exact pair-overlap
   elementary moments, while degree-one decay does not control degree two.

The machine JSON records four proof DAGs, four discarded routes, four single
successor lemmas, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-235 Schur complements, prime-power deficits, phase retrieval, and CRT overlaps](schur-primepower-phase-overlap.md).
한국어 보고서(`parent conjecture claims blocked · open_not_proven`): [TICKET-235 Schur 보완·prime-power 결손·위상 복원·CRT overlap](schur-primepower-phase-overlap.ko.md).

## Preserved TICKET-234 continuation: operator kernels, binary affine sieves, Goldbach half-channels, and Poisson CRT degrees

TICKET-234 proves four exact partial, equivalence, or no-go theorems and keeps
the parent-conjecture resolution count at zero:

1. RH: a logarithmic scalar diagonal floor can coexist with a singular full
   Gram form, and an arbitrarily small unstructured signed tail can be negative
   on its kernel.
2. Collatz: every fixed finite affine-modulus sieve has infinitely many
   primitive binary density-band false positives, so the next divisor must be
   word-adaptive.
3. Goldbach: the strict full minor margin is endpoint-equivalent; same-half
   prime squares have exact major-minor cancellation, leaving reflected
   low-high cross phase as the decisive channel.
4. Twin Prime: critical CRT noise tends to zero exactly when all fixed-degree
   moving-coordinate Cesaro square correlations do; fixed-labelled decay is
   insufficient.

The machine JSON records four proof DAGs, four discarded routes, four single
successor lemmas, zero conjecture resolutions, and zero computational failures.

English report: [TICKET-234 operator kernels, binary affine sieves, Goldbach half-channels, and Poisson CRT degrees](operator-kernel-density-minor-cesaro.md).
한국어 보고서: [TICKET-234 연산자 영공간·이진 affine sieve·Goldbach half-channel·Poisson CRT](operator-kernel-density-minor-cesaro.ko.md).

## Preserved: TICKET-230 quantitative recurrence, necklaces, Fourier aggregation, and centering

TICKET-230 audits the four successor targets from TICKET-229 before attempting
stronger analytic estimates. It proves four exact structural or no-go
statements and keeps the parent-conjecture resolution count at zero:

1. RH: simultaneous Dirichlet approximation forces every fixed finite
   `m`-dilation family to have an unbounded near-alias sequence with energy
   `O(T^(-2/m))`. Any slower-decaying global finite-family floor is impossible;
   an adaptive or infinite frame matched to the actual Weil tail remains open.
2. Collatz: `2^(a_0)B(rho a)=3B(a)+D`, so both `D|B` and `gcd(D,B)` are
   invariant under cyclic rotation. Rotation searches must be quotiented by
   necklaces; global representative nondivisibility and aperiodic descent
   remain open.
3. Goldbach: the exact family `w_m=1+m delta_a` on `Z/m^2Z` has every
   nonprincipal Fourier mode `o(W)` while all target phases align to produce
   an error of principal-term size. Modewise decay alone cannot prove
   pointwise positivity; a signed aggregate prime minor-arc estimate remains
   open.
4. Twin Prime: on shift-two admissible residues modulo five, the raw quadratic
   character has exact mean `1/3`, not zero. The previous uncentered target is
   refuted and replaced by centered Type-II saving at the twin-sieve main
   scale, still requiring a positive principal lower bound.

Machine audit: four exact partial or no-go theorems, four rejected or corrected
routes, four proof DAGs, zero conjecture resolutions, and zero computational
failures.

English report: [TICKET-230 quantitative recurrence, necklace invariance, Fourier aggregation, and local centering](quantitative-recurrence-necklace-fourier-centering.md).
한국어 보고서: [TICKET-230 정량 재귀·목걸이 불변성·푸리에 합산·국소 중심화](quantitative-recurrence-necklace-fourier-centering.ko.md).

## TICKET-237 continuation: principal angles, finite palettes, dyadic endpoints, and Welch floors

TICKET-237 attacks the four TICKET-236 successor lemmas and keeps the
parent-conjecture resolution count at zero:

1. RH: the normalized Gram cross block is the principal-angle matrix.
   Strict contraction is equivalent to disjoint spans with positive angle;
   nested cofinal spans have norm one. The open target is an arithmetic
   innovation-angle gap after quotienting common logarithmic modes.
2. Collatz: for every finite prime palette, an lcm of the relevant
   multiplicative orders disables every palette prime at infinitely many
   binary run blocks. A word-dependent valuation-gap witness on general
   primitive density-band necklaces remains open.
3. Goldbach: truncation at `X` gives the exact endpoint identity
   `g_X(2X)=1_P(X)`. A closed dyadic window containing `2X` cannot support
   a uniform inverse-log phase margin. A buffered bulk phase gain remains
   open.
4. Twin Prime: a support-rank argument gives the sharp Welch floor
   `E_(m,2)>=(m-r)/(r(m-1))`. Degree-two decay with nondegenerate diagonals
   forces growing support, but the prime-weighted decay, positive mass, and
   parity transfer remain open.

Each proof DAG declares the exact theorem, reproducible rational or modular
audit, no-go scope, discarded route, and one successor lemma. Machine audit:
four exact partial/no-go theorems, four discarded routes, four proof DAGs,
zero conjecture resolutions, and zero computational failures.

English report: [TICKET-237 principal angles, finite palettes, dyadic endpoints, and Welch floors](angle-palette-endpoint-welch.md).
한국어 보고서(`parent conjecture claims blocked · open_not_proven`): [TICKET-237 principal angle·유한 palette·dyadic endpoint·Welch floor](angle-palette-endpoint-welch.ko.md).

## TICKET-236 continuation: normalized contractions, order witnesses, reflected phase defects, and degree-two CRT reduction

TICKET-236 attacks the four TICKET-235 successor lemmas and keeps the
parent-conjecture resolution count at zero:

1. RH: for positive diagonal blocks, full block positivity is exactly the
   normalized cross-block contraction condition. The family
   `A=C=I_m`, `B=(2/m)J_m` has every coordinate minor positive and entries
   tending to zero, but minimum eigenvalue `-1`; local-minor certification is
   therefore refuted. Arithmetic contraction on actual Weil frames is open.
2. Collatz: the primes `5`, `59`, and `57,653` give order-separated witnesses
   for every binary run-block exponent not divisible by `28,826`. At multiples
   of `28,826` all three divide both denominator and numerator, so this fixed
   palette is rigorously exhausted. A fresh adaptive witness beyond every
   finite palette is open.
3. Goldbach: for the actual prime indicator, reflected phase defect and the
   Goldbach representation count obey the exact complementary identity
   `q g_X(N)=q pi(X)-Delta_X(N)`. The fixed target `N=4` has normalized margin
   `1/pi(X)`, refuting an uncoupled inverse-log margin. Target-coupled dyadic
   phase gain remains open.
4. Twin Prime: covariance positivity gives
   `E_{m,1} <= sqrt(4/m+(m-1)E_{m,2}/m)`, and a collision estimate bounds every
   fixed `E_{m,k}` by degree two plus `O_k(1/m)`. Independent all-degree proof
   obligations are reduced to prime-weighted degree-two decay, which is open.

Each proof DAG has a declared target, exact symbolic or order argument,
reproducible finite audit, explicit finite-computation boundary, discarded
route, and one successor lemma. Machine audit: four exact partial/reduction/
no-go theorems, four discarded or reduced routes, four proof DAGs, zero
conjecture resolutions, and zero computational failures.

English report: [TICKET-236 normalized contractions, order witnesses, reflected phase defects, and degree-two reduction](contraction-order-phase-degree2.md).
한국어 보고서(`parent conjecture claims blocked · open_not_proven`): [TICKET-236 정규화 수축·차수 증인·반사 위상 결손·2차 환원](contraction-order-phase-degree2.ko.md).

## TICKET-238 continuation: multishell accumulation, valuation quantifiers, mesoscopic buffers, and effective rank

TICKET-238 audits the four TICKET-237 successors without claiming a parent
solution.

1. **Riemann:** a normalized cross-block row sum below one is sufficient for
   multishell positivity. Uniform pairwise angle gaps do not force a strict
   global lower bound: at `rho=1/3,J=4`, `K_ij=-rho` is the jointly
   realizable regular-simplex Gram matrix with positive two-shell blocks but
   zero global eigenvalue. Larger `J` rows are abstract block systems. The
   next obligation is
   `ArithmeticWeilInnovationNormalizedCrossRowSumBelowOneOnCofinalDisjointLogarithmicShells`.
2. **Collatz:** `D not dividing B` is exactly equivalent to an adaptive prime
   valuation deficit. TICKET-197 therefore closes this certificate for every
   run block, but the all-necklace version is not weaker than universal affine
   nondivisibility. The next obligation is
   `RunBlockValuationWitnessEscapesEveryFixedFinitePrimePalette`.
3. **Goldbach:** `g_X(2X-h)<=h+1`, so an inverse-log normalized margin requires
   `h` at least on the `X/(log X)^2` scale. The next obligation is
   `MesoscopicBufferedDyadicReflectedPrimeCrossPhaseGainWithIndependentMinorSlack`.
4. **Twin Prime:** degree-two energy tends to zero exactly when normalized Gram
   effective rank diverges. A growing-support, fixed-effective-rank family
   refutes support growth as sufficient. The next obligation is
   `PrimeWeightedDegreeTwoCRTGramEffectiveRankDivergesWithUniformDiagonalControl`.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
machine failures, and zero conjecture resolutions.

English report: [TICKET-238 multishell, valuation, buffer, and effective-rank audit](multishell-valuation-buffer-effectiverank.md).
한국어 보고서: [TICKET-238 다중 shell·valuation·buffer·유효랭크 감사](multishell-valuation-buffer-effectiverank.ko.md).
## TICKET-239 continuation: cancellation, lifting, Fourier reflection, and CRT parity

TICKET-239 attacks the four TICKET-238 successors without claiming a parent
solution.

1. **Riemann.** Proved a power-decay Schur threshold and constructed a
   uniformly positive normalized Gram family with divergent absolute row sums.
   This refutes absolute summability as a necessary Weil-positivity condition.
2. **Collatz.** Proved the exact local lifting-defect dichotomy controlling
   valuation witnesses on common multiples. The scan of 17,982 odd primes
   through 200,000 found no positive defect but remains finite evidence.
3. **Goldbach.** Proved the exact mesoscopic reflection Fourier identity and a
   same-cardinality, same-Parseval-energy zero-reflection counterfamily.
4. **Twin prime.** Proved the uniform CRT admissibility Gram matrix is the
   identity while every admissible residue class still contains infinitely
   many pairs with both entries composite.

The four next nodes require arithmetic or signed transfer: Weil cross-block
Cotlar-Stein cancellation, nonpositive run-block lifting defect for every odd
prime, mesoscopic signed Fourier slack above negative DC, and parity-sensitive
prime-weighted CRT transfer to positive twin mass.

Machine audit: four exact theorems, four rejected routes, four proof DAGs, zero
machine failures, and zero conjecture resolutions.

English report: [TICKET-239 cancellation, lifting, Fourier, and CRT audit](cancellation-lifting-fourier-crt.md).
한국어 보고서: [TICKET-239 상쇄·lifting·Fourier·CRT 감사](cancellation-lifting-fourier-crt.ko.md).

## TICKET-240 continuation: route correction, Wieferich depth, and one-sided prime CRT

TICKET-240 audits the four TICKET-239 successors and corrects three targets
that were not genuinely weaker than their parent obligation.

1. **Riemann.** A uniformly positive Gram family has divergent Cotlar
   square-root overlap sums. Absolute Cotlar summability is sufficient when
   available but is neither necessary nor sign-sensitive.
2. **Collatz.** The local run-block defect is exactly the difference between
   the rational Wieferich depths of 32/27 and 2/3 at exponent q-1.
   The scan of 1,270,605 primes through 20,000,000 finds no positive candidate
   but does not discharge the universal quantifier.
3. **Goldbach.** The proposed signed remainder threshold above negative DC is
   exactly R_A(h)>=1 by integrality. The next target must expose an
   independently positive main term and explicit errors.
4. **Twin prime.** CRT and Dirichlet prove that every complete finite local
   pattern contains infinitely many primes p whose successor p+2 is
   composite. One-sided prime weighting therefore cannot break parity.

Machine audit: four exact theorems, four route corrections, four proof DAGs,
zero machine failures, and zero conjecture resolutions.

English report: [TICKET-240 route corrections, Wieferich depths, and prime-weighted CRT](route-corrections-wieferich-prime-crt.md).
한국어 보고서: [TICKET-240 경로 교정·Wieferich 깊이·소수 가중 CRT](route-corrections-wieferich-prime-crt.ko.md).

## TICKET-241 continuation: finite information, canonical errors, and fixed-base search

TICKET-241 audits the four TICKET-240 successors and removes four finite or
decomposition-dependent signals that cannot carry the required infinite
arithmetic content.

1. **Riemann.** Proved that every finite unsigned prime-cosine kernel is PSD
   with rank at most twice its prime support. Any lower floor on the forced
   nullspace comes exactly from an added diagonal and does not establish the
   complete signed Guinand-Weil form.
2. **Collatz.** Constructed an exact principal-unit countermodel to the desired
   Fermat-line implication for every odd prime q>5. Separately scanned all
   5,761,453 primes through 100,000,000 for the actual bases, with zero
   candidates; the universal fixed-base implication remains open.
3. **Goldbach.** Proved that signed error control is the target identity itself,
   while absolute-error control is only sufficient and can be made arbitrarily
   bad by a canceling refinement unless the arc contract and norm are fixed.
4. **Twin prime.** Proved by CRT and Dirichlet that every finite periodic
   fingerprint has infinitely many prime inputs with a composite shift-two
   successor, so fixed finite feature enrichment cannot break parity.

Machine audit: four exact theorems, four rejected or narrowed routes, four proof
DAGs, zero machine failures, and zero conjecture resolutions.

English report: [TICKET-241 finite information, canonical errors, and fixed-base search](finite-information-canonical-errors.md).
한국어 보고서: [TICKET-241 유한 정보·정규 오차·고정 밑수 탐색](finite-information-canonical-errors.ko.md).

## TICKET-242 continuation: quantifiers, order cores, Parseval scale, and diagonal CRT

TICKET-242 attacks the four TICKET-241 successors and closes four strictly
weaker boundary statements without resolving any parent conjecture.

| Track | Exact theorem now closed | Route discarded | Next single lemma |
|---|---|---|---|
| RH | PointwiseFiniteSectionMovingVectorNoGoAndCompactUniformTransfer | pointwise fixed-test convergence as growing-family positivity | UniformSignedGuinandWeilTailBoundOnFrequencyTightNormalizedAdmissibleTestClasses |
| Collatz | RationalWieferichOrderCoreReductionAndBoundedOrderNoGo | bounded multiplicative orders as an all-prime proof | UniformOrderCoreSquareDivisorTransferFrom32Over27To2Over3 |
| Goldbach | ParsevalScaleObstructionToL2OnlyBinaryMinorArcCertificates | global L2 plus triangle inequality at the natural binary scale | FixedBinaryPrimeMinorArcCoefficientIsLittleOOfTargetMainUniformlyOnBufferedEvenTargets |
| Twin | GrowingPeriodDiagonalCRTMimicryForShiftTwo | modulus growth alone as a parity-breaking certificate | ScaleLocalGrowingModulusTypeIICancellationForShiftTwoLambdaWithPositivePrimeMass |

The RH moving-vector model is an abstract quantifier counterexample, not an
actual Guinand-Weil finite section. The Collatz scan through 200,000 only
replays the exact LTE identity; TICKET-241 contains the larger 100,000,000
candidate search. The Goldbach table illustrates the Parseval scale mismatch
but proves no targetwise signed saving. The Twin witnesses are not placed in
predeclared dyadic blocks and give no quantitative least-prime bound.

Machine artifact:
data/open-problem/ticket242-quantifier-order-parseval-diagonal-crt.json.
Reports: [English](quantifier-order-parseval-diagonal-crt.md) and
[한국어](quantifier-order-parseval-diagonal-crt.ko.md).

## TICKET-243 continuation: bandlimit, principal units, half-arc energy, and dyadic mimicry

This iteration attacks exactly one successor lemma per problem and resolves no
parent conjecture.

1. **Riemann.** `BandlimitedEvenTestFamilyNoncompactnessAndFrequencyTightnessNoGo`
   constructs a normalized real-even orthonormal family with one fixed Fourier
   support, plus a smooth separated subsequence. Frequency tightness alone is
   therefore not the compactness premise required by TICKET-242.
2. **Collatz (deep focus).** `UnboundedOrderPrincipalUnitTransferCountermodels`
   uses Teichm�ller lifts to construct, for every prime `q>5`, a local model
   of order `(q-1)/2` in which the `(5,-3)` square-depth condition holds
   but the `(1,-1)` condition fails. This refutes universal local transfer,
   not the special fixed bases `32,27`.
3. **Strong Goldbach.** `OmittedHalfFrequencyArcCarriesNaturalBinaryEnergy`
   proves an absolute energy floor `(pi(X)-3)^2/(12X)` on the parity-frequency
   arc. A circle-method decomposition must cover that arc as major or exploit
   signed targetwise cancellation.
4. **Twin Prime.** `FixedPeriodicMimicryInEverySufficientlyLargeDyadicBlock`
   combines CRT with fixed-modulus PNT in arithmetic progressions. Its
   threshold depends on the fixed modulus, so growing-modulus Type II
   cancellation remains open.

The bounded replay scans 5,130 primes through `q=50,000`, with zero model
certificate failures. The analytic theorems do not depend on that finite
range. The machine-readable audit, four proof DAGs, exact next lemmas, and
claim boundaries are in
`data/open-problem/ticket243-bandlimit-principal-unit-half-arc-dyadic-mimicry.json`.
## TICKET-244 continuation: joint tightness, harmonic bad lines, parity folding, and polylog mimicry

TICKET-244 attacks the four TICKET-243 successors and closes four strictly
bounded statements without resolving a parent conjecture:

1. joint physical-frequency tails characterize relative compactness in bounded
   `L2(R)` families; physical-only and frequency-only compactness both fail;
2. the fixed-base first Wieferich bad line is exactly
   `4H_floor(q/3)=5H_((q-1)/2) mod q`; simultaneous first-layer vanishing does
   not decide higher valuations;
3. the odd-prime even-target Goldbach integrand is exactly half-periodic and,
   for even `N>=6`, has the full-prime binary coefficient;
4. for every fixed `A`, any pure periodic Twin fingerprint with
   `M_X<=(log_2 X)^A` has prime/composite-successor mimics in every sufficiently
   large dyadic block, by Bertrand, CRT, and uniform Siegel-Walfisz.

The deep-focus result is item 4 and is classified `exact_no_go`. Items 1-3 are
`partial_theorem`. The exact generator, five track/integrated JSON artifacts,
eight focused tests, bilingual proof, proof DAGs, and persistent state are linked
from
`data/open-problem/ticket244-joint-tightness-harmonic-parity-fold-polylog-mimicry.json`.
All four conjectures remain `open_not_proven`.

## TICKET-245 continuation: closure margins, second Fermat digits, Klein arc orbits, and Linnik-height mimicry

TICKET-245 attacks the four TICKET-244 successors and closes four strictly
bounded statements without resolving a parent conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `ClosureZeroSetObstructionToUniformWeilMargin` | discard joint-tightness plus pointwise/classwise positivity without closure separation | `ZeroFreeClosureSeparationForNormalizedAdmissibleWeilFunctional` |
| Collatz | `SecondOrderFixedBaseFermatDigitCriterion` | retain exact fixed-base higher-digit analysis; finite nonoccurrence is not a theorem | `FixedBaseAllPrimeRationalWieferichDepthDomination` |
| Goldbach | `KleinFourOrbitReductionForEvenGoldbachArcs` | discard independent estimation of four symmetry-related rational arcs | `UniformRepresentativeArcAsymptoticAndSignedResidualSavingOnQuarterTorus` |
| Twin | `PolynomialHeightPeriodicMimicryFromLinnik` | discard a fixed periodic classifier sound beyond every polynomial height | `ScaleLocalNonperiodicTypeIICancellationBeyondPeriodicHeightBarriers` |

The deep-focus Twin theorem fixes `M,a,F` before using two Bertrand primes,
CRT, and Linnik's least-prime theorem. It gives no prescribed-dyadic-block
uniformity for a changing modulus. The Collatz scan covers 1,270,604 primes
through twenty million, but it is adversarial finite evidence only. All four
proof DAGs have one open frontier, and all parent conjectures remain
`open_not_proven`.

Machine artifact:
`data/open-problem/ticket245-closure-second-order-klein-linnik.json`.
Reports: [English](closure-second-order-klein-linnik.md) and
[한국어](closure-second-order-klein-linnik.ko.md).
## TICKET-246 continuation: finite moments, all-depth algebra, center Parseval, and prime-power contamination

TICKET-246 advances each TICKET-245 frontier by one exact, falsifiable auxiliary
statement and resolves no parent conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `FiniteEvenMomentAnnihilatorNoGo` | discard separation by a fixed finite even-moment list on the model class | `InfiniteFeatureCoercivityOnNormalizedAdmissibleWeilClosure` |
| Collatz | `AllDepthFixedBaseFermatPolynomialIdentity` | retain exact fixed-base valuation analysis; finite histograms prove no all-prime order | `FixedBaseAllPrimeValuationDominationForPqByUqMinusVq` |
| Goldbach | `RationalCenterResidueParsevalBridge` | discard the Ramanujan mean with its residue residual omitted | `UniformQuarterTorusResidueVarianceDecayWithArcStability` |
| Twin | `PrimePowerPairProxyContaminationBound` | discard uncorrected equality of prime-power pairs and twin pairs | `ScaleLocalTypeIILowerBoundBeyondPrimePowerContamination` |

The deep-focus Collatz identity is exact at arbitrary q-adic depth because the
two binomial expansions terminate; the 17,981-prime replay is only an
adversarial check. The Twin domain is odd starts `n>=3`: an initial broader
domain was rejected by the boundary counterexample `(2,4)`. Each proof DAG
has one open frontier, and all parent conjectures remain `open_not_proven`.

Machine artifact:
`data/open-problem/ticket246-moment-alldepth-parseval-primepower.json`.
Reports: [English](moment-alldepth-parseval-primepower.md) and
[한국어](moment-alldepth-parseval-primepower.ko.md).

## TICKET-247 continuation: Hilbert-Schmidt, Hensel, arc Lipschitz, and sharp prime powers

TICKET-247 attacks the four TICKET-246 frontiers with exact compactness,
`q`-adic, Fourier-displacement, and prime-power counting arguments. It resolves
no parent conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `HilbertSchmidtInfiniteMomentCoercivityNoGo` | discard every summable weighted-moment coercivity bound on the full even L2 sphere | `NonHilbertSchmidtArithmeticWeilCoercivityOnAdmissibleClosure` |
| Collatz | `FormalHenselBranchNoGoForValuationDomination` | discard valuation domination derived from the unrestricted polynomial identity alone | `ArithmeticFermatQuotientExclusionOfPqHenselBranch` |
| Goldbach | `RationalCenterArcLipschitzBridgeAndCenterOnlyNoGo` | discard center-only uniform arc promotion; retain an explicit first-moment term | `UniformSignedResidueVarianceAndFirstMomentSavingOnQuarterTorus` |
| Twin | `SharpOddPrimePowerContaminationBound` | replace the exponent-blind correction by the exact exponent count and square/cube bound | `ScaleLocalTypeIILowerBoundBeyondSharpPrimePowerContamination` |

The RH theorem is infinite but scoped: it uses every summable weight sequence
on the full even L2 model and does not identify the genuine Weil closure. The
Collatz theorem is also all-prime/all-depth but uses unrestricted q-adic pairs,
not actual Fermat quotients. Goldbach retains the necessary frequency-scale
term, and Twin still lacks a lower bound beyond contamination. Every proof DAG
has one open frontier; all parent conjectures remain `open_not_proven`.

Machine artifact:
`data/open-problem/ticket247-hilbert-hensel-lipschitz-primepower.json`.
Reports: [English](hilbert-hensel-lipschitz-primepower.md) and
[한국어](hilbert-hensel-lipschitz-primepower.ko.md).

## TICKET-248 continuation: unweighted moments, Wieferich separation, centered first jets, and active contamination

TICKET-248 attacks the four TICKET-247 frontiers with an explicit noncompact
escape sequence, exact Fermat-quotient congruences, a centered Fourier first
jet, and two-event inclusion-exclusion. It resolves no parent conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `UnweightedInfiniteMomentCoercivityNoGo` | discard raw unweighted infinite-moment coercivity on the full even L2 sphere | `ArithmeticOffDiagonalWeilCoercivityOnAdmissibleClosure` |
| Collatz | `ActualBadBranchGeneralizedWieferichSeparation` | retain the exact separated-prime criterion; discard promotion of finite no-hits | `ExistenceOfSeparatedGeneralizedWieferichPrimeFor32Over27Against2Over3` |
| Goldbach | `CenteredFirstJetParsevalArcBridge` | retain exact mean-square first-jet control; discard uniform numerator promotion without a maximal estimate | `UniformReducedNumeratorCenteredFirstJetSavingOnQuarterTorus` |
| Twin | `ExactActivePrimePowerContaminationIdentity` | replace all-prime-power counting by exact active shift-two support | `ScaleLocalTypeIILowerBoundBeyondActivePrimePowerContamination` |

The RH theorem is infinite but remains scoped to the full even L2 model, not
the genuine Guinand-Weil admissible closure or its arithmetic off-diagonal
form. The Collatz scan through one million primes, the Goldbach denominator
table through 96, and the twin audit through ten million are finite replay
certificates only. The Goldbach identity is aggregate rather than
numerator-uniform, and the twin identity supplies no Type-II lower bound.
Every proof DAG has one open frontier; all parent conjectures remain
`open_not_proven`.

Machine artifact:
`data/open-problem/ticket248-unweighted-wieferich-jet-active.json`.
Reports: [English](unweighted-wieferich-jet-active.md) and
[한국어](unweighted-wieferich-jet-active.ko.md).
## TICKET-249 continuation: compact perturbations, projective slopes, Parseval spikes, and even-left classification

TICKET-249 attacks the four TICKET-248 frontiers with compact-operator
functional analysis, projective Fermat quotients, an exact Fourier spike
countermodel, and a Diophantine classification. It resolves no parent
conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `CompactOffDiagonalMomentCoercivityNoGo` | discard repair of raw full-sphere moment coercivity by any compact quadratic perturbation | `NoncompactArithmeticWeilFormOrLegendreExclusion` |
| Collatz | `SeparatedWieferichProjectiveSlopeCriterion` | retain the exact nonzero slope `[3:5]`; discard promotion of finite no-hits | `OccurrenceOrAvoidanceOfProjectiveFermatQuotientSlopeThreeFifths` |
| Goldbach | `CenteredJetParsevalSpikeNoGo` | discard uniform numerator saving from centeredness and aggregate Parseval alone | `PrimeSpecificReducedNumeratorJetAntiConcentration` |
| Twin | `EvenExponentLeftActiveContaminationClassification` | classify away-from-three even-left support as the unique pair `25 -> 27`; right support remains open | `ScaleLocalRightActivePrimePowerContaminationBound` |

The RH compactness theorem is infinite but scoped to the full even L2 model;
it neither identifies the genuine Weil form as compact nor places the
Legendre sequence in the admissible closure. The Collatz ten-million-prime
scan and finite-field exhaustive tables are finite replay only. The Goldbach
countermodel is an abstract centered residue vector, not a vector of prime
counts. The Twin theorem uses the published Lebesgue-Nagell classification of
`x^2+2=y^n` as an explicit external theorem node and gives no right-active or
Type-II estimate. Every proof DAG has one open frontier; all parent
conjectures remain `open_not_proven`.

Machine artifact:
`data/open-problem/ticket249-compact-projective-parseval-lebesgue.json`.
Reports: [English](compact-projective-parseval-lebesgue.md) and
[한국어](compact-projective-parseval-lebesgue.ko.md).

## TICKET-250 continuation: multiplier escape, lift transitivity, Galois support, and even-left classification

TICKET-250 attacks the four TICKET-249 frontiers and resolves no parent
conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `NoncompactMultiplierLegendreEscapeInsufficiencyNoGo` | discard Legendre-only noncompact coercivity validation; retain simultaneous oscillation/concentration control | `ArithmeticWeilFormCoercivityAgainstOscillationAndConcentrationEscapes` |
| Collatz | `LocalFermatQuotientLiftTransitivityNoGo` | discard lift-invariant local slope avoidance; retain canonical representatives | `CanonicalRepresentativeFermatQuotientDistributionBeyondLiftTransitivity` |
| Goldbach | `PrimeModulusRationalFourierFullSupportAndNormBarrier` | exclude the exact rational two-spike model at prime q>=5; retain quantitative upper anti-concentration | `QuantitativePrimeCountFourierEnergyAntiConcentrationAtPrimeModuli` |
| Twin | `AllBaseEvenLeftRightActiveClassification` | close all even-left support as `25 -> 27`; retain odd-left contamination | `ScaleLocalOddLeftRightActiveContaminationBound` |

The infinite RH no-go is scoped to `M_(x^2)` on the full even L2 model, not
the actual Weil form. The infinite Collatz no-go concerns all local lifts, not
canonical occurrence across primes or all trajectories. The Goldbach theorem
proves exact support and nonzero norm, not a quantitative upper saving or a
log-weighted estimate. The Twin theorem uses the published D=2
Lebesgue-Nagell classification as an explicit external node and gives no
odd-left or Type-II estimate. All parent problems remain `open_not_proven`.

Machine artifact:
`data/open-problem/ticket250-multiplier-lift-galois-evenright.json`.
Reports: [English](multiplier-lift-galois-evenright.md) and
[한국어](multiplier-lift-galois-evenright.ko.md).
## TICKET-251 continuation: interior concentration, finite-prime CRT, cyclotomic concentration, and a right-even modulo-eight constraint

TICKET-251 attacks the four TICKET-250 frontiers and resolves no parent
conjecture.

| Track | Exact theorem now closed | Route discarded or retained | Next single lemma |
|---|---|---|---|
| RH | `InteriorZeroLocalMultiplierCoercivityNoGo` | discard every continuous nonnegative local multiplier with an interior zero as a full-sphere repair | `NonlocalArithmeticWeilKernelExcludesInteriorConcentration` |
| Collatz | `FinitePrimeCanonicalLiftPatternCRTInterpolationNoGo` | discard inference from any finite lift-compatible prime set; retain fixed canonical representatives | `CanonicalRepresentativeFermatQuotientDistributionBeyondFiniteCRTInterpolation` |
| Goldbach | `CyclotomicUnitFullSupportEnergyConcentrationNoGo` | discard structural-only anti-concentration from integrality, full support, and norm | `ActualPrimeCountResidueVectorsExcludeCyclotomicUnitConcentration` |
| Twin | `RightEvenModuloEightConstraintAndSharpness` | retain the necessary odd-k, p=7 mod 8 condition; discard any claim that congruence alone forces k=1 | `NoPositivePrimePowerSolutionsOfXSquareMinusTwoEqualsYOddPower` |

The RH and Goldbach no-go theorems are analytic all-parameter statements; their
finite rows only replay exact examples. The Collatz CRT theorem applies to
every finite prime set but changes the integer representatives with that set,
so it does not determine `F_q(2),F_q(3)`. The Twin theorem is elementary and
only proves a modulo-eight condition; the withdrawn `x^2-2=y^n` source is not
a dependency, and the all-X odd-exponent Diophantine exclusion remains open. Every proof DAG has exactly one open frontier. All
four parent problems remain `open_not_proven`.

Machine artifact:
`data/open-problem/ticket251-interior-crt-cyclotomic-righteven.json`.
Reports: [English](interior-crt-cyclotomic-righteven.md) and
[한국어](interior-crt-cyclotomic-righteven.ko.md).
