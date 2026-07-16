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
  "CO-TICKET-127 corrects the base exception: for n>1, finite-stopping counterexamples are exactly nontrivial eventually-low paths; the fixed n=1 path survives every tree and is not a counterexample"

def topAttackTheoremTicket : String :=
  "CO-TICKET-128 UniformNontrivialEventuallyLowPathExclusion."

def topAttackProofAttemptProtocol : String :=
  "Exclude every nontrivial eventually-low infinite path in the exact adaptive unresolved tree by a uniform rank or descent argument; retain the fixed n=1 basin path and do not mistake arbitrary 2-adic paths for positive-integer counterexamples."

def latestExactResult : String :=
  "NontrivialEventuallyLowPathIffFiniteStoppingCounterexample, with 4027109 nontrivial unresolved odd classes among 134217728 at precision 28 after removing the fixed n=1 path"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "uniform exclusion of nontrivial eventually-low unresolved paths"

end PrimeProject.OpenProblems.Collatz
