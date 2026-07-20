namespace PrimeProject.OpenProblems.Collatz

def missingInfiniteBridge : String :=
  "formal residue-cover descent theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ResidueRankDescentCover implies primeproject_collatz_conjecture"

def requiredProofObjects : List String := [
  "exact valuation cylinders and affine thresholds",
  "finite exception termination certificates",
  "well-founded unbounded-depth contracting cover of every natural valuation code"
]

def theoremDecomposition : List String := [
  "CO-TD1 NaturalCollatzCodesAreCountableDenseAndNull closed",
  "CO-TD2 ContractingValuationCylinderLeastCounterexampleExclusion closed",
  "CO-TD3 NoBoundedDepthContractingPrefixCover closed",
  "CO-TD4a MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover closed",
  "CO-TD4b NaturalCodesCrossAffineDescentThreshold highest_risk_open",
  "CO-TD5 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-135 NaturalCodesCrossAffineDescentThreshold."

def topAttackProofAttemptProtocol : String :=
  "Use an ordinal or rank argument allowing unbounded adaptive depth; every finite maximum depth is defeated by the exact all-one expanding cylinder n=-1 mod 2^(K+1)."

def latestExactResult : String :=
  "MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover: almost every odd 2-adic valuation code eventually has 2^S>3^k, but natural codes are a dense null set and slope contraction is not affine descent"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "every actual natural valuation code crosses both the negative-slope condition and its exact positive affine descent threshold"

end PrimeProject.OpenProblems.Collatz
