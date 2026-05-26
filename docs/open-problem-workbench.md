# Open Problem Proof Workbench

PrimeProject now has four GitHub Pages subpages for:

- Riemann Hypothesis
- Collatz Conjecture
- Goldbach Conjecture
- Twin Prime Conjecture

The purpose is not to publish a fake proof. The workbench is a disciplined proof lab: each page shows finite evidence, a bounded certificate, a proof-attempt ledger, a proof attack map, a machine proof-status gate, a proof execution protocol, a proof frontier probe, a known-barrier audit, a formal replay package, a proof review docket, a proof reduction contract, proof candidate intake rules, proof attempt execution logs, a proof obligation DAG, a Lean-oriented formal proof contract, a proof milestone queue, a decisive lemma lab with certified automated falsification probes, a proof-gap taxonomy, the missing infinite proof gates, candidate strategies, and blocked claim language. The public claim level is `proof_workbench_only`.

## Public Pages

- `open-problems/riemann.html`
- `open-problems/collatz.html`
- `open-problems/goldbach.html`
- `open-problems/twin-prime.html`

All four pages read `data/open_problem_workbench.json` through the same GitHub Pages public JSON path.

## Generated Evidence

Regenerate the bounded evidence bundle:

```powershell
python scripts/generate_open_problem_workbench.py --limit 1000000 --output data/open_problem_workbench.json
```

Verify the committed bounded certificates:

```powershell
python scripts/verify_open_problem_workbench.py
```

Current bounded checks:

- Riemann: prime-counting and Chebyshev theta diagnostics through 1,000,000.
- Collatz: exhaustive trajectory replay for start values through 1,000,000.
- Goldbach: exhaustive even-number decomposition check through 1,000,000.
- Twin Prime: twin-pair counts and Hardy-Littlewood heuristic comparison through 1,000,000.

Each problem includes a `primeproject.bounded-proof-certificate.v1` object. The certificate hashes every bounded witness or diagnostic row, groups leaves into deterministic chunks, and exposes a Merkle root that CI recomputes. This is a real proof artifact for the bounded theorem only. It is intentionally not a proof of the unbounded conjecture.

Each problem also includes a `primeproject.proof-attempt-ledger.v1` object. The ledger separates three things:

- `proved_by_certificate`: the finite theorem already verified by the Merkle certificate.
- `open_obligation`: the exact infinite lemma still needed before any solution claim is allowed.
- `falsification_targets`: concrete ways an attempted proof can fail.

The same ledger now includes an attack graph, known theorem bridges, and lemma candidates. This is the proof-search contract for each problem:

- The attack graph shows which edge still has to remove the finite search limit.
- Known theorem bridges record where existing mathematics is usable, insufficient, or only heuristic.
- Lemma candidates state the next target in a form that could later be moved into a formal proof assistant.

Each problem also includes a `primeproject.open-problem-proof-status-gate.v1` object. The gate is intentionally conservative: it blocks a full-proof claim while any obligation, attack-graph edge, theorem bridge, or lemma candidate remains open. `scripts/verify_open_problem_workbench.py` checks that all four pages remain blocked until the finite certificate is joined to an independently checkable infinite proof.

Each problem also includes a `primeproject.proof-execution-protocol.v1` object. This protocol turns the proof attempt into ordered execution stages: bounded certificate replay, formal target normalization, decisive lemma attack, gap work-order falsification, and full-proof promotion. Each stage names its required output and verifier, and the protocol keeps `blocked_before_full_proof` until the machine gate becomes eligible for independent review.

Each problem also includes a `primeproject.proof-frontier-probe.v1` object. This is the computational pressure test for the current proof frontier: Riemann stresses theta-envelope candidates at prime endpoints, Collatz stresses accelerated odd residue descents, Goldbach ranks hard residue classes by first-prime witness, and Twin Prime separates exact gap-2 residue persistence from bounded-gap evidence. The probe status is always `finite_probe_not_proof`; it can falsify or prioritize a proof path but cannot close the conjecture.

Each problem also includes a `primeproject.known-barrier-audit.v1` object. This audit lists barriers that routinely invalidate attempted proofs: finite-to-infinite lifting, proof-assistant replay, RH-equivalence strength, Collatz exceptional residue classes, Goldbach positive lower bounds, Twin Prime exact-gap lower bounds, and heuristic dependencies. A page remains blocked while any barrier lacks a formal clearance artifact.

Each problem also includes a `primeproject.formal-replay-package.v1` object. This package names the Lean-oriented files, replay commands, required artifacts, and forbidden tokens that would be needed before any candidate proof can be submitted for independent review. Its status remains `not_replayable_until_barriers_clear` while known barriers are open.

Each problem also includes a `primeproject.proof-review-docket.v1` object. The docket acts like a reviewer checklist: the bounded theorem is accepted only for the committed finite limit, while the full conjecture claim, formal replay readiness, and barrier clearance remain rejected or blocked until the proof-status gate can be promoted.

Each problem also includes a `primeproject.proof-reduction-contract.v1` object. The contract states the smallest theorem package that would make a full-proof claim reviewable, separates accepted partial results from the target conjecture, and lists forbidden shortcuts such as replacing strong Goldbach with weak Goldbach or replacing exact twin gaps with bounded gaps.

Each problem also includes a `primeproject.proof-candidate-intake.v1` object. The intake rules say what a future proof candidate must submit, which executable tests run first, and which shortcuts cause automatic rejection before review.

Each problem also includes a `primeproject.proof-attempt-execution-log.v1` object. The log records executed proof routes, the machine checks applied to each route, the bounded or rejected result, the failure reason, and the exact next artifact required before the route can be promoted.

Each problem also includes a `primeproject.proof-obligation-dag.v1` object. The DAG links attempts, proof gaps, milestones, the decisive reduction theorem, and the open target claim so that every remaining proof obligation is visible as a node with a required artifact and dependency edge.

Each problem also includes a `primeproject.formal-proof-contract.v1` object. The contract records a Lean 4 target theorem, required artifacts, forbidden assumptions, and acceptance rules. This is not a formal proof yet; it is the kernel-facing contract that any future proof must satisfy before the status gate can move.

Each problem also includes a `primeproject.proof-milestone-queue.v1` object. The queue turns the proof contract into work items: the bounded certificate is the only completed milestone, while formal definitions, infinite bridge theorems, and independent kernel review remain open or blocked.

Each problem also includes a `primeproject.decisive-lemma-lab.v1` object. This is the current proof-forge target: it names the single lemma that would close the most important open milestones, records the finite probe that PrimeProject can already replay, and states the proof obligation and falsification test that prevent finite evidence from being misrepresented as a full solution. The same object now carries an automated falsification probe with bounded pass conditions, violation counts, strongest observed stress cases, the explicit proof gap that keeps the problem open, and a `primeproject.decisive-lemma-probe-certificate.v1` hash certificate over the probe payload.

The decisive lemma lab also carries a `primeproject.proof-gap-taxonomy.v1` object. This breaks the remaining proof gap into named open or blocked items such as infinite-lift, theorem-bridge, formalization, dependency-control, and independent-review gaps. Each gap must name the artifact needed to close it, the next experiment to run, and the failure signal that would invalidate that path.

## Claim Boundary

The pages must keep these claims blocked:

- unverified full-proof claim for the Riemann Hypothesis
- unverified full-proof claim for the Collatz conjecture
- unverified full-proof claim for the Goldbach conjecture
- unverified full-proof claim for the Twin Prime conjecture

Finite computation can disprove a universal conjecture if it finds a counterexample, but it cannot prove these universal or infinitude statements by itself. Any future promotion from `open_not_proven` requires an independently checkable argument that removes the search limit.

## Research Direction

The next useful step is to convert repeated empirical structure into explicit lemmas:

- Riemann: identify a residual law strong enough to imply a known RH equivalence, then prove it analytically.
- Collatz: build residue-block descent certificates and prove recursive coverage of all blocks.
- Goldbach: find the thinnest representation classes and turn the lower-bound heuristic into an explicit positive lower bound.
- Twin Prime: isolate admissible two-point patterns and search for a lower-bound theorem that proves infinitely many exact gap-2 pairs.
