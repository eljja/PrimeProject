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
  "GB-TICKET-121 preserves joint balanced signed cancellation; the Twin balance-angle defect result does not transfer across problems"

def topAttackTheoremTicket : String :=
  "GB-TICKET-122 JointBalancedVaughanGoldbachResidualEnvelope."

def topAttackProofAttemptProtocol : String :=
  "For U,V at most N^(1/3), prove (<I,Lambda_reflect>-M)+<II,Lambda_reflect> >= -K*M/log(N) jointly; reject cutoffs whose Type II support collapses."

end PrimeProject.OpenProblems.Goldbach
