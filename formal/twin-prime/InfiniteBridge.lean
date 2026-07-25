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
  "TP-TD3b.2b.3 UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass highest_risk_open",
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
  "TP-TICKET-139 UniformSobolevAperiodicTypeIICancellationWithPositiveTwinMass."

def topAttackProofAttemptProtocol : String :=
  "Fix one scale-uniform Sobolev or variation budget, prove signed Type II cancellation inside that class, and transport the estimate to positive exact-gap-two mass."

def latestFiniteResult : String :=
  "FiniteIrrationalOrbitLipschitzLookupComplexityNoGo: every finite labeling has a tent interpolant with Lipschitz constant at most 2/delta, while a closest-pair labeling needs at least 1/delta"

def finiteEvidenceBoundary : String :=
  "the exact no-go excludes scale-dependent Lipschitz lookup as a proof step, but does not prove that actual twin-prime labels have large complexity or establish Type II cancellation"

def retainedOpenPremise : String :=
  "a scale-uniform Sobolev aperiodic Type II cancellation theorem, signed transport, and positive exact-gap-two mass"

end PrimeProject.OpenProblems.TwinPrime
