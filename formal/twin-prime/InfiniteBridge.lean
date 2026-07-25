namespace PrimeProject.OpenProblems.TwinPrime

def missingInfiniteBridge : String :=
  "formal exact gap-2 lower-bound theorem"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExactGapTwoLowerBoundBridge implies primeproject_twin_prime_conjecture"

def requiredProofObjects : List String := [
  "scale-growing exact-pair selector weight family",
  "near-full-scale parity-sensitive separation from quantitative primorial composite lifts",
  "infinitude bridge from positive exact-gap lower bound"
]

def theoremDecomposition : List String := [
  "TP-TD1 EveryAdmissibleFiniteResidueClassHasInfiniteCompositePairLifts closed",
  "TP-TD2 ScaleDependentPrimorialCompositeLiftBound closed",
  "TP-TD3a FiniteCongruenceTranscriptCompositeLift closed",
  "TP-TD3b.1 FiniteRationalFourierAlgebraCompositeLift closed",
  "TP-TD3b.2a RationalFourierInformationBudgetLowerBound closed",
  "TP-TD3b.2b.1 IrrationalInjectivityWithoutRegularityIsTautologicalNoGo closed",
  "TP-TD3b.2b.2 FiniteIrrationalOrbitLipschitzLookupComplexityNoGo closed",
  "TP-TD3b.2b.3 QuadraticIrrationalSobolevRotationCancellation closed",
  "TP-TD3b.2b.4a QuadraticIrrationalBilinearLargeSieveCancellation closed",
  "TP-TD3b.2b.4b UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass superseded_circular_target",
  "TP-TD3b.2b.5a CubicRoughnessLiouvilleExactTwinProjector closed",
  "TP-TD3b.2b.5b OneSidedCubicRoughLiouvilleLedgerGap superseded_exactly_equivalent_to_block_twin_positivity",
  "TP-TD3b.2b.6a WalshHadamardRoughPairInversionAndCircularGapNoGo closed",
  "TP-TD3b.2b.6b UniformCubicRoughWalshL1ContractionBelowOne highest_risk_open",
  "TP-TD4 PositiveExactGapLowerBound",
  "TP-TD5 ExactGapInfinitudeBridge"
]

def breakthroughObjectBlueprint : String :=
  "TP-TD2 exact-pair parity witness that survives semiprime countermodels"

def counterexampleGuidedSynthesis : String :=
  "Twin Prime CEGIS: generate exact-pair weights, reject parity-model and wider-gap leakage"

def rankedCegisTarget : String :=
  "TP-TICKET-128 gives an exact endpoint-only countermodel and proves that a within-dyadic-block envelope yields limsup Q<=0.92*c+delta"

def topAttackTheoremTicket : String :=
  "TP-TICKET-143 UniformCubicRoughWalshL1ContractionBelowOne."

def topAttackProofAttemptProtocol : String :=
  "Prove a fixed-delta absolute contraction |A10|+|A01|+|A11|<=(1-delta)A00 on every sufficiently large cubic-rough pair block."

def latestFiniteResult : String :=
  "WalshHadamardRoughPairInversionAndCircularGapNoGo: all four rough-pair parity classes invert exactly, and the prior one-sided gap is exactly four times the twin count"

def finiteEvidenceBoundary : String :=
  "four finite blocks satisfy an absolute Walsh L1 contraction, but they supply no uniform all-scale delta"

def retainedOpenPremise : String :=
  "a uniform parity-sensitive absolute Walsh-correlation contraction on cubic-rough pairs"

end PrimeProject.OpenProblems.TwinPrime
