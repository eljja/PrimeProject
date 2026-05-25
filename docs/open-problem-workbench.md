# Open Problem Proof Workbench

PrimeProject now has four GitHub Pages subpages for:

- Riemann Hypothesis
- Collatz Conjecture
- Goldbach Conjecture
- Twin Prime Conjecture

The purpose is not to publish a fake proof. The workbench is a disciplined proof lab: each page shows finite evidence, a bounded certificate, a proof-attempt ledger, a proof attack map, a machine proof-status gate, a Lean-oriented formal proof contract, a proof milestone queue, a decisive lemma lab with certified automated falsification probes, the missing infinite proof gates, candidate strategies, and blocked claim language. The public claim level is `proof_workbench_only`.

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

Each problem also includes a `primeproject.formal-proof-contract.v1` object. The contract records a Lean 4 target theorem, required artifacts, forbidden assumptions, and acceptance rules. This is not a formal proof yet; it is the kernel-facing contract that any future proof must satisfy before the status gate can move.

Each problem also includes a `primeproject.proof-milestone-queue.v1` object. The queue turns the proof contract into work items: the bounded certificate is the only completed milestone, while formal definitions, infinite bridge theorems, and independent kernel review remain open or blocked.

Each problem also includes a `primeproject.decisive-lemma-lab.v1` object. This is the current proof-forge target: it names the single lemma that would close the most important open milestones, records the finite probe that PrimeProject can already replay, and states the proof obligation and falsification test that prevent finite evidence from being misrepresented as a full solution. The same object now carries an automated falsification probe with bounded pass conditions, violation counts, strongest observed stress cases, the explicit proof gap that keeps the problem open, and a `primeproject.decisive-lemma-probe-certificate.v1` hash certificate over the probe payload.

## Claim Boundary

The pages must keep these claims blocked:

- Riemann Hypothesis proven
- Collatz Conjecture proven
- Goldbach Conjecture proven
- Twin Prime Conjecture proven

Finite computation can disprove a universal conjecture if it finds a counterexample, but it cannot prove these universal or infinitude statements by itself. Any future promotion from `open_not_proven` requires an independently checkable argument that removes the search limit.

## Research Direction

The next useful step is to convert repeated empirical structure into explicit lemmas:

- Riemann: identify a residual law strong enough to imply a known RH equivalence, then prove it analytically.
- Collatz: build residue-block descent certificates and prove recursive coverage of all blocks.
- Goldbach: find the thinnest representation classes and turn the lower-bound heuristic into an explicit positive lower bound.
- Twin Prime: isolate admissible two-point patterns and search for a lower-bound theorem that proves infinitely many exact gap-2 pairs.
