namespace PrimeProject.OpenProblems.TwinPrime

def replayStatus : String := "not_replayable_until_barriers_clear"
def publicClaim : String := "bounded_theorem_only"
def targetTheoremName : String := "primeproject_twin_prime_conjecture"
def targetTheoremStatement : String :=
  "theorem primeproject_twin_prime_conjecture : forall N : Nat, exists p : Nat, N < p /\\ Nat.Prime p /\\ Nat.Prime (p + 2) := by"

end PrimeProject.OpenProblems.TwinPrime
