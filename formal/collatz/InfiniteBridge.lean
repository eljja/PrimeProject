namespace PrimeProject.OpenProblems.Collatz

def missingInfiniteBridge : String :=
  "formal residue-cover descent theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ResidueRankDescentCover implies primeproject_collatz_conjecture"

def requiredProofObjects : List String := [
  "finite accelerated residue partition",
  "well-founded rank definition",
  "edge-by-edge exact descent certificate"
]

def theoremDecomposition : List String := [
  "CO-TD1 AcceleratedResiduePartition",
  "CO-TD2 WellFoundedResidueRank",
  "CO-TD3 EveryEdgeDescendsOrEntersBasin highest_risk_open",
  "CO-TD4 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-125 proves universal finite stopping descent is equivalent to Collatz and certifies 121825 of 131072 odd 18-bit residue cylinders, leaving 9247 unresolved"

def topAttackTheoremTicket : String :=
  "CO-TICKET-126 AdaptiveResidueFiniteStoppingCover."

def topAttackProofAttemptProtocol : String :=
  "Recursively refine only unresolved residue cylinders, prove every positive-integer branch receives a finite exact descent certificate, and treat every nonterminating refinement lineage as a candidate counterexample to the cover rather than as a Collatz counterexample."

end PrimeProject.OpenProblems.Collatz
