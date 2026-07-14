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
  "CO-TICKET-119 preserves the exact golden-mean escape target; no Twin 16M scale-persistence shortcut is imported"

def topAttackTheoremTicket : String :=
  "CO-TICKET-120 GoldenMeanInvariantSetEscape."

def topAttackProofAttemptProtocol : String :=
  "Prove the exact logarithmic tail orbit exits the no-00 subshift infinitely often, or construct a compatible infinite avoiding path and test whether it is realized by a positive integer orbit."

end PrimeProject.OpenProblems.Collatz
