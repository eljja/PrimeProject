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
  "CO-TD4b.2b.1 SubcriticalPeriodicValuationCodesHaveNoPositiveNaturalEmbedding closed",
  "CO-TD4b.2b.2 CollatzCycleDiophantineWindowAndVerifiedFloorExclusion closed",
  "CO-TD4b.2b.3 FixedCycleMinimumWindowEventuallyVacuousNoGo closed",
  "CO-TD4b.2b.4a PeriodDependentFloorLinearGrowthBarrier closed",
  "CO-TD4b.2b.4b CycleMinimumAboveExactPowerOfTwoWindowThreshold highest_risk_open",
  "CO-TD4b.2b.5 AffineCappedAperiodicNaturalCodeWellFoundedness open",
  "CO-TD5 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-141 CycleMinimumAboveExactPowerOfTwoWindowThreshold."

def topAttackProofAttemptProtocol : String :=
  "Prove that every hypothetical k-cycle minimum exceeds the exact threshold determined by 2^ceil(k log_2 3)/3^k; subcritical-linear floor growth is insufficient."

def latestExactResult : String :=
  "PeriodDependentFloorLinearGrowthBarrier: avoiding automatic product-window vacuity requires asymptotic minimum-floor slope at least 1/(3 log 2)"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "cycle minima beat the exact power-of-two approximation threshold period by period, and every aperiodic affine-capped natural code has a global well-founded descent certificate"

end PrimeProject.OpenProblems.Collatz
