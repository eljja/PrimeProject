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
  "TP-TD3b.2b IrrationalOrSupercriticalAperiodicTypeIITwinSeparation highest_risk_open",
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
  "TP-TICKET-137 IrrationalOrSupercriticalAperiodicTypeIITwinSeparation."

def topAttackProofAttemptProtocol : String :=
  "Build irrational or supercritical aperiodic Type II information that does not factor through a subcritical rational denominator lcm, distinguish the n<2Lrs composite collisions, and transport a signed lower bound to positive exact-gap-two mass."

def latestFiniteResult : String :=
  "RationalFourierInformationBudgetLowerBound: denominator lcm L has an in-range composite-pair collision whenever 2*L*r*s<=X"

def finiteEvidenceBoundary : String :=
  "the information-budget theorem excludes transcript-only rational Fourier sufficient certificates when 2*L*r*s<=X, but not external arithmetic data, irrational phases, supercritical periods, or analytic Type II information; it is not a Twin Prime counterexample"

def retainedOpenPremise : String :=
  "an irrational or supercritical aperiodic factor-sensitive Type II separator, its signed transport, and positive exact-gap-two mass"

end PrimeProject.OpenProblems.TwinPrime
