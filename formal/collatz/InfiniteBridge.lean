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
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-129 UnboundedPrefixClosureOrUniformNontrivialPathRank."

def topAttackProofAttemptProtocol : String :=
  "Promote finite prefix closure to every precision by a uniform rank, or preserve any bounded step-cap survivor as a replayable candidate; retain the fixed n=1 basin path."

def latestExactResult : String :=
  "FinitePrefixEventuallyLowExclusion: all 4027109 nontrivial unresolved representatives below 2^28 descend directly; maximum accelerated stopping time is 249 at 217740015"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "unbounded prefix closure or a uniform well-founded rank excluding every nontrivial eventually-low path"

end PrimeProject.OpenProblems.Collatz
