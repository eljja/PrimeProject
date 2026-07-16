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
  "GB-TICKET-125 proves the exact endpoint budget A-K/log(H)-B*log(H)^2/sqrt(H)>0 at the verified H=4e18, while leaving A K B unproved"

def topAttackTheoremTicket : String :=
  "GB-TICKET-126 ExplicitJointBalancedGoldbachCutoff."

def topAttackProofAttemptProtocol : String :=
  "Derive replayable uniform constants A K B for the weighted major lower bound, joint signed Vaughan residual, and proper-prime-power contamination, then verify the strict endpoint budget at H=4e18."

end PrimeProject.OpenProblems.Goldbach
