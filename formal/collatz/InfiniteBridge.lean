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
  "CO-TICKET-124 reclassifies GoldenMeanInvariantSetEscape as a Mersenne-delay route lemma rather than a sufficient global Collatz bridge"

def topAttackTheoremTicket : String :=
  "CO-TICKET-125 ResidueRankDescentCover."

def topAttackProofAttemptProtocol : String :=
  "Synthesize a finite accelerated residue partition and well-founded rank whose every edge descends or enters the verified basin; use any uncovered residue or nondecreasing reachable SCC as a counterexample to the proposed cover."

end PrimeProject.OpenProblems.Collatz
