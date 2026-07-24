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
  "CO-TD4b.1 LeastCounterexampleAffineCorrectionInequality closed",
  "CO-TD4b.2a AffineCappedValuationCylinderMassDecay closed",
  "CO-TD4b.2b ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet highest_risk_open",
  "CO-TD5 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-137 ArithmeticEmptinessOfInfiniteAffineCappedNaturalCodeSet."

def topAttackProofAttemptProtocol : String :=
  "Combine the exact affine cap with natural-residue stabilization and an Archimedean well-founded rank to exclude every infinite natural valuation code; exponentially small 2-adic mass and any fixed finite depth are insufficient."

def latestExactResult : String :=
  "AffineCappedValuationCylinderMassDecay: least-counterexample prefix caps have exponentially decaying 2-adic Haar mass, but every finite cylinder still has arbitrarily large natural representatives"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "the infinite affine-capped survivor set contains no valuation code of any positive natural integer"

end PrimeProject.OpenProblems.Collatz
