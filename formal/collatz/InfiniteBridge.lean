namespace PrimeProject.OpenProblems.Collatz

def missingInfiniteBridge : String :=
  "formal residue-cover descent theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ResidueRankDescentCover implies primeproject_collatz_conjecture"

def requiredProofObjects : List String := [
  "exact valuation cylinders and affine thresholds",
  "finite exception termination certificates",
  "prefix-free contracting cover of every natural valuation code"
]

def theoremDecomposition : List String := [
  "CO-TD1 NaturalCollatzCodesAreCountableDenseAndNull closed",
  "CO-TD2 ContractingValuationCylinderLeastCounterexampleExclusion closed",
  "CO-TD3 PrefixFreeContractingCylinderCoverOfEveryNaturalCode highest_risk_open",
  "CO-TD4 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-133 PrefixFreeContractingCylinderCoverOfEveryNaturalCode."

def topAttackProofAttemptProtocol : String :=
  "Extend only noncontracting exact cylinders, discharge every finite threshold exception, and prove that each natural code reaches a contracting prefix; a finite observed tree is not a cover theorem."

def latestExactResult : String :=
  "ContractingValuationCylinderLeastCounterexampleExclusion: a word with 2^S>3^k has an exact finite non-descent set in its natural residue cylinder; 3861 of 3905 audited words reduce to the single unique exception n=1"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "an adaptive prefix-free contracting-cylinder cover for every actual natural code"

end PrimeProject.OpenProblems.Collatz
