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
  "TP-TD3b.2b.4b UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass highest_risk_open",
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
  "TP-TICKET-141 UniformMinorArcVaughanBilinearCancellationWithPositiveTwinMass."

def topAttackProofAttemptProtocol : String :=
  "Extend the fixed sqrt(2) bilinear large-sieve estimate uniformly across the required minor arcs, insert the actual Vaughan or Mobius coefficients, and preserve a positive exact-gap-two main term."

def latestFiniteResult : String :=
  "QuadraticIrrationalBilinearLargeSieveCancellation: arbitrary separable coefficients at the fixed sqrt(2) phase gain the balanced relative factor sqrt(5/L)"

def finiteEvidenceBoundary : String :=
  "the exact theorem treats one fixed quadratic-irrational phase, but not uniform minor arcs, the full Vaughan or Mobius decomposition, the sieve parity obstruction, or positive gap-two mass"

def retainedOpenPremise : String :=
  "uniform minor-arc large-sieve cancellation for the actual arithmetic Type II coefficients, signed transport, and positive exact-gap-two mass"

end PrimeProject.OpenProblems.TwinPrime
