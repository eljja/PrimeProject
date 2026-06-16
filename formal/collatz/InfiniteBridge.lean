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
  "CO-CEGIS-13 attack_next"

def topAttackTheoremTicket : String :=
  "CO-TICKET-13 NineCircuitCycleDiophantineExclusion: Steiner's nine-circuit cycle equation and p-adic distance bounds have no positive integer solutions within the certified continued fractions limit."

def topAttackProofAttemptProtocol : String :=
  "Formulate the nine-circuit cycle equation with nine independent odd blocks; evaluate continued fraction convergents of ln(3)/ln(2) and compute p-adic valuation bounds; verify that no integer solutions exist for b1 + ... + b9 <= 2000 using arbitrary-precision solver."

end PrimeProject.OpenProblems.Collatz
