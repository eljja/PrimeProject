namespace PrimeProject.OpenProblems.Goldbach

def missingInfiniteBridge : String :=
  "formal large-even threshold theorem with explicit cutoff"

def bridgeStatus : String := "open_infinite_bridge"

def nextAIDiscoveryTheorem : String :=
  "ExplicitGoldbachCutoffBridge implies primeproject_goldbach_conjecture"

def requiredProofObjects : List String := [
  "explicit major/minor arc inequality budget",
  "verified finite overlap certificate",
  "N0 comparison below the certified finite range"
]

def theoremDecomposition : List String := [
  "GB-TD1 ExplicitTwoPrimeBudget",
  "GB-TD2 ErrorTermsReplayable",
  "GB-TD3 CutoffBelowFiniteCertificate highest_risk_open",
  "GB-TD4 FiniteLargeNGlue"
]

def breakthroughObjectBlueprint : String :=
  "GB-TD3 explicit inequality budget with certified cutoff below finite range"

def counterexampleGuidedSynthesis : String :=
  "Goldbach CEGIS: generate explicit budgets, reject unsourced constants and cutoffs above finite range"

def rankedCegisTarget : String :=
  "GB-TICKET-124 requires joint pointwise Vaughan residual control to be coupled to an explicit positive major term, cutoff, and finite-overlap bridge"

def topAttackTheoremTicket : String :=
  "GB-TICKET-125 ExplicitJointBalancedGoldbachCutoff."

def topAttackProofAttemptProtocol : String :=
  "For U,V at most N^(1/3), prove a joint pointwise residual bound with explicit K, show the positive major term dominates above an explicit N0 below 4e18, and glue to the verified finite range without collapsed Type II support."

end PrimeProject.OpenProblems.Goldbach
