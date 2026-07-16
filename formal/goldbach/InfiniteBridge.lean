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
  "GB-TICKET-126 proves the proper-prime-power contamination bound with uniform B=2.0949181787429647 at H=4e18, leaving only the major constant A and signed residual constant K open"

def topAttackTheoremTicket : String :=
  "GB-TICKET-127 ExplicitGoldbachMajorAndResidualConstants."

def topAttackProofAttemptProtocol : String :=
  "Derive replayable uniform constants A and K for the weighted major lower bound and joint signed Vaughan residual, reuse the proved B contamination bound, and verify A-K/log(H)-B*log(H)^2/sqrt(H)>0 at H=4e18."

def latestExactResult : String :=
  "ExplicitProperPrimePowerContaminationBound: Q(N) <= sqrt(N)+(floor(log_2 N)-2)*N^(1/3), hence B=2.0949181787429647 uniformly above H=4e18"

def closedPremise : String :=
  "proper-prime-power contamination constant B"

def retainedOpenPremise : String :=
  "explicit weighted major constant A and joint signed residual constant K"

end PrimeProject.OpenProblems.Goldbach
