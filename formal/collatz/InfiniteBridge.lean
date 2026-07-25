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
  "CO-TD4b.2b.4b CycleMinimumAboveExactPowerOfTwoWindowThreshold superseded_wrong_direction",
  "CO-TD4b.2b.5a PrimitiveCycleSuccessorDistinctProductUpperBoundAndTargetCollapseNoGo closed",
  "CO-TD4b.2b.5b Period15601AffineNumeratorNondivisibilityCertificate retired_below_published_odd_period_floor",
  "CO-TD4b.2b.6a PublishedOddPeriodFloorRetiresPeriod15601AndCompositionExplosionNoGo closed",
  "CO-TD4b.2b.6b PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness highest_risk_open",
  "CO-TD5 CycleAndDivergenceExclusionBridge"
]

def breakthroughObjectBlueprint : String :=
  "CO-TD3 residue-debt automaton plus exact SCC descent certificate"

def counterexampleGuidedSynthesis : String :=
  "Collatz CEGIS: generate residue-rank candidates, reject uncovered blocks and nondecreasing SCCs"

def rankedCegisTarget : String :=
  "CO-TICKET-128 separates unresolved lift cylinders from integer candidates and directly closes all 4027109 nontrivial 28-bit frontier representatives"

def topAttackTheoremTicket : String :=
  "CO-TICKET-143 PublishedFloorAwareAffineCappedNaturalCodeWellFoundedness."

def topAttackProofAttemptProtocol : String :=
  "Import the published odd-cycle period floor explicitly, then build an unbounded-depth well-founded descent certificate for natural valuation codes without spending computation below that floor."

def latestExactResult : String :=
  "PublishedOddPeriodFloorRetiresPeriod15601AndCompositionExplosionNoGo: the cited K>7.2e10 odd-member floor retires period 15601, whose raw ordered valuation space already has 7069 decimal digits"

def retiredRoute : String :=
  "treating the boundary ray -3^{-1} in Z_2 as a natural-integer obstruction"

def retainedOpenPremise : String :=
  "cycles beyond the published odd-period floor and a global well-founded descent certificate for every aperiodic natural valuation code"

end PrimeProject.OpenProblems.Collatz
