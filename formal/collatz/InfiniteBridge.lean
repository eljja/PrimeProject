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
  "CO-TICKET-126 proves that a positive integer lacks finite stopping descent exactly when its inverse-limit residue path is an eventually-low infinite path in the adaptive unresolved tree"

def topAttackTheoremTicket : String :=
  "CO-TICKET-127 UniformEventuallyLowPathExclusion."

def topAttackProofAttemptProtocol : String :=
  "Exclude every eventually-low infinite path in the exact adaptive unresolved tree by a uniform rank or descent argument; do not mistake arbitrary 2-adic paths or the non-natural boundary ray for positive-integer counterexamples."

def latestExactResult : String :=
  "EventuallyLowUnresolvedPathIffFiniteStoppingCounterexample, with 4027110 unresolved odd classes among 134217728 at precision 28 and no finite-to-infinite inference"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "uniform exclusion of eventually-low unresolved paths"

end PrimeProject.OpenProblems.Collatz
