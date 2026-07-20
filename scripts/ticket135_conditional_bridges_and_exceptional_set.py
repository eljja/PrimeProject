from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket132_admissibility_nullset_hard_stratum_local_parity import (
    crt,
    first_primes_above,
    fraction_payload,
)


GENERATED_AT = "2026-07-21T01:15:00+09:00"
SCHEMA = "primeproject.ticket135-conditional-bridges-and-exceptional-set.v1"
K56_MARGIN = Fraction(23_019_645_297, 2_140_000_000_000)


def sharp_block_tail_positivity() -> dict[str, Any]:
    examples = [
        (Fraction(2), Fraction(3), Fraction(2)),
        (Fraction(1), Fraction(4), Fraction(2)),
        (Fraction(3, 2), Fraction(5, 2), Fraction(1)),
    ]
    rows = []
    failures = 0
    for alpha, gamma, beta in examples:
        margin = alpha * gamma - beta * beta
        rows.append(
            {
                "alpha": fraction_payload(alpha),
                "gamma": fraction_payload(gamma),
                "beta": fraction_payload(beta),
                "schur_margin": fraction_payload(margin),
                "certificate_accepts": margin >= 0,
            }
        )
        failures += int(alpha < 0 or gamma < 0 or margin < 0)

    bad_alpha = Fraction(1)
    bad_gamma = Fraction(1)
    bad_beta = Fraction(3, 2)
    bad_margin = bad_alpha * bad_gamma - bad_beta * bad_beta
    witness = (bad_beta, bad_alpha)
    witness_value = bad_alpha * bad_margin
    failures += int(bad_margin >= 0)
    failures += int(witness_value >= 0)

    return {
        "theorem_name": "SharpBlockTailPositivityCertificate",
        "title_ko": "샤프한 블록-꼬리 양성 인증 정리",
        "declared_target": (
            "Prove a dimension-independent sufficient condition for attaching an "
            "uncomputed self-adjoint tail to a certified finite Weil Gram core."
        ),
        "proved_statement": (
            "Let H=F direct-sum T and M=[[A,B],[B*,C]] be self-adjoint. If "
            "A>=alpha I, C>=gamma I, ||B||<=beta, alpha,gamma>=0, and "
            "beta^2<=alpha*gamma, then M>=0. The threshold is sharp for the "
            "class determined only by these three constants: when alpha>0 and "
            "beta^2>alpha*gamma, the scalar block [[alpha,-beta],[-beta,gamma]] "
            "has a strict negative direction."
        ),
        "proved_statement_ko": (
            "자기수반 블록 연산자 M에서 유한 코어 A의 하한 alpha, 꼬리 C의 "
            "하한 gamma, 교차항 B의 노름 상한 beta가 beta^2<=alpha*gamma를 "
            "만족하면 전체 M은 양의 준정부호이다. 이 세 상수만 사용하는 "
            "판정으로는 이 경계가 최적이다."
        ),
        "proof": (
            "For u=||x|| and v=||y||, the quadratic form is at least "
            "alpha*u^2-2*beta*u*v+gamma*v^2. If alpha>0, completing the "
            "square gives alpha*(u-beta*v/alpha)^2+"
            "(gamma-beta^2/alpha)*v^2>=0. The alpha=0 case forces beta=0 "
            "and is immediate. Conversely, for the scalar block and vector "
            "(beta,alpha), the quadratic value is alpha*(alpha*gamma-beta^2)<0."
        ),
        "exact_certificate_contract": {
            "finite_core_lower_bound": "A>=alpha I",
            "tail_lower_bound": "C>=gamma I",
            "cross_norm_bound": "||B||<=beta",
            "acceptance_inequality": "beta^2<=alpha*gamma",
            "sharp_countermodel_when_violated": "[[alpha,-beta],[-beta,gamma]]",
        },
        "rational_audit": {
            "accepted_rows": rows,
            "violating_example": {
                "alpha": fraction_payload(bad_alpha),
                "gamma": fraction_payload(bad_gamma),
                "beta": fraction_payload(bad_beta),
                "schur_margin": fraction_payload(bad_margin),
                "negative_witness": [str(value) for value in witness],
                "witness_value": fraction_payload(witness_value),
            },
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "certified finite-core lower bounds plus explicit tail and cross-block operator bounds",
            "discard": "finite Gram positivity without a tail lower bound and cross-block norm estimate",
            "next_theorem": "ProjectedWeilBlockConstantsWithPositiveSchurMargin",
        },
        "machine_audit": {
            "accepted_example_count": len(rows),
            "sharp_negative_example_verified": witness_value < 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The operator inequality is exact and dimension independent, but no "
            "published Weil normalization is shown here to supply alpha, gamma, "
            "and beta with positive Schur margin. It therefore does not prove RH."
        ),
    }


def collatz_survival_audit(maximum_depth: int = 64) -> dict[str, Any]:
    states: dict[int, Fraction] = {0: Fraction(1)}
    previous_survival = Fraction(1)
    selected_depths = {1, 2, 4, 8, 16, 32, maximum_depth}
    rows = []
    failures = 0
    for depth in range(1, maximum_depth + 1):
        maximum_surviving_sum = (3**depth).bit_length() - 1
        next_states: dict[int, Fraction] = {}
        for total, mass in states.items():
            for valuation in range(1, maximum_surviving_sum - total + 1):
                next_total = total + valuation
                next_states[next_total] = next_states.get(next_total, Fraction(0)) + mass / (2**valuation)
        survival = sum(next_states.values(), Fraction(0))
        crossing = previous_survival - survival
        failures += int(survival < 0 or survival >= previous_survival)
        failures += int(crossing + survival != previous_survival)
        if depth in selected_depths:
            rows.append(
                {
                    "depth": depth,
                    "maximum_noncontracting_sum": maximum_surviving_sum,
                    "surviving_state_count": len(next_states),
                    "survival_mass": fraction_payload(survival),
                    "first_crossing_mass_at_depth": fraction_payload(crossing),
                    "cumulative_crossing_mass": fraction_payload(1 - survival),
                }
            )
        states = next_states
        previous_survival = survival
    return {
        "maximum_depth": maximum_depth,
        "selected_rows": rows,
        "final_survival_mass": fraction_payload(previous_survival),
        "strictly_decreasing_through_audited_depth": failures == 0,
        "failure_count": failures,
    }


def collatz_full_measure_prefix_cover() -> dict[str, Any]:
    finite_audit = collatz_survival_audit()
    failures = finite_audit["failure_count"]
    return {
        "theorem_name": "MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover",
        "title_ko": "최소 음의-기울기 접두사의 전측도 prefix-free 덮개 정리",
        "declared_target": (
            "Determine exactly how far the TICKET134 unbounded-prefix route can be "
            "completed in the odd 2-adic probability space."
        ),
        "proved_statement": (
            "Under normalized Haar measure on the odd 2-adic integers, accelerated "
            "Collatz valuations a_j are independent with P(a_j=m)=2^-m. Almost "
            "every valuation code has a first k with 2^(a_1+...+a_k)>3^k. The "
            "minimal such words are prefix-free and their cylinder masses sum to one."
        ),
        "proved_statement_ko": (
            "홀수 2-adic 정수의 Haar 확률에서 가속 콜라츠 valuation은 "
            "P(a_j=m)=2^-m인 독립 확률변수다. 거의 모든 코드는 최초로 "
            "2^(a_1+...+a_k)>3^k가 되는 접두사를 가지며, 그 최소 접두사들은 "
            "서로 prefix-free이고 cylinder 질량의 합은 1이다."
        ),
        "proof": (
            "A length-k valuation cylinder has conditional odd-Haar mass "
            "2^-(a_1+...+a_k), which factors into the geometric laws. Hence the "
            "strong law gives (a_1+...+a_k)/k -> E[a_1]=2. Since "
            "2>log_2(3), the strict inequality is eventually reached almost surely. "
            "Taking the first crossing makes the cylinders disjoint and prefix-free; "
            "their union has measure one, so their Kraft mass is one."
        ),
        "exact_probability_contract": {
            "alphabet": "positive valuations m>=1",
            "letter_probability": "P(a_j=m)=2^-m",
            "word_mass": "2^-(a_1+...+a_k)",
            "slope_crossing": "2^(sum a_j)>3^k",
            "law_of_large_numbers_gap": "E[a_j]-log_2(3)=2-log_2(3)>0",
        },
        "finite_dynamic_program_audit": finite_audit,
        "route_decision": {
            "retain": "separate full-measure slope contraction from the pointwise affine descent threshold on natural codes",
            "discard": "promoting an almost-everywhere 2-adic cover to every positive integer",
            "next_theorem": "NaturalCodesCrossAffineDescentThreshold",
        },
        "machine_audit": {
            "audited_depth": finite_audit["maximum_depth"],
            "survival_mass_decreases": finite_audit["strictly_decreasing_through_audited_depth"],
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The natural positive odd integers form a countable dense Haar-null set, "
            "so they could lie inside the exceptional null set. Moreover a slope "
            "below one does not by itself beat the positive affine term for a given "
            "integer. This theorem is not a pointwise Collatz descent proof."
        ),
    }


def goldbach_hard_stratum_moment_bridge() -> dict[str, Any]:
    rows = []
    failures = 0
    for exponent in [8, 16, 32, 64, 128]:
        hard_size = exponent - 1
        ceiling_log2 = (hard_size - 1).bit_length()
        moment = 4 * ceiling_log2
        inflation = hard_size ** (1.0 / moment)
        failures += int(moment <= 0 or inflation >= 6 / 5)
        rows.append(
            {
                "horizon": f"2^{exponent}",
                "power_of_two_hard_stratum_size": hard_size,
                "moment_order": moment,
                "supremum_inflation_factor": inflation,
                "below_six_fifths": inflation < 6 / 5,
            }
        )
    rational_guard = Fraction(6, 5) ** 4 - 2
    threshold = Fraction(5, 6) * K56_MARGIN
    failures += int(rational_guard <= 0)
    return {
        "theorem_name": "SparseHardStratumMomentToMaximumBridge",
        "title_ko": "희소 난층의 모멘트-최댓값 연결 정리",
        "declared_target": (
            "Replace the TICKET134 global log-scale moment requirement by the exact "
            "moment scale needed after restricting to the sparse Goldbach hard stratum."
        ),
        "proved_statement": (
            "For a function r on a finite set H of size h>=2 with normalized L^p "
            "norm, ||r||_infinity<=h^(1/p)||r||_p, and the constant is sharp. If "
            "p=4*ceil(log_2 h), then h^(1/p)<6/5. Therefore "
            "||r||_p<=(5/6)m_56 implies ||r||_infinity<m_56. For powers of two "
            "up to X, h=O(log X), so this sufficient moment order is O(log log X)."
        ),
        "proved_statement_ko": (
            "원소 수가 h인 유한 hard stratum에서 정규화 L^p 노름은 "
            "||r||_infinity<=h^(1/p)||r||_p를 만족하며 상수는 최적이다. "
            "p=4 ceil(log_2 h)이면 팽창계수는 6/5보다 작다. 따라서 이 "
            "희소층에서 (5/6)m_56 이하의 모멘트 상계는 m_56 미만의 "
            "점별 상계로 승격된다."
        ),
        "proof": (
            "The largest summand is at most the sum of the p-th powers, giving "
            "the norm inequality; a one-point spike gives equality. Put "
            "m=ceil(log_2 h). Then h<=2^m and p=4m, so "
            "h^(1/p)<=2^(1/4)<6/5 because (6/5)^4>2. Multiplying by the "
            "assumed (5/6)m_56 bound gives a strict m_56 supremum bound."
        ),
        "exact_bridge_contract": {
            "K56_margin": fraction_payload(K56_MARGIN),
            "sufficient_Lp_threshold": fraction_payload(threshold),
            "moment_order": "p=4*ceil(log_2 h)",
            "sharp_norm_inequality": "||r||_infinity<=h^(1/p)||r||_p",
            "rational_guard": fraction_payload(rational_guard),
        },
        "finite_scale_audit": {"rows": rows, "failure_count": failures},
        "route_decision": {
            "retain": "prove moments directly on a rigorously defined minimal-main hard stratum",
            "discard": "global sublogarithmic moments and any norm-to-pointwise claim without the h^(1/p) factor",
            "next_theorem": "BinaryGoldbachHardStratumLogMomentBoundK56",
        },
        "machine_audit": {
            "audited_scale_count": len(rows),
            "six_fifths_guard_verified": rational_guard > 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a sharp deterministic norm bridge. It supplies no estimate for "
            "the actual binary Goldbach residual on the hard stratum and therefore "
            "proves no Goldbach representation."
        ),
    }


def lcm_many(moduli: Iterable[int]) -> int:
    result = 1
    for modulus in moduli:
        result = math.lcm(result, modulus)
    return result


def first_admissible_residues(modulus: int, count: int) -> list[int]:
    residues = []
    for residue in range(modulus):
        if math.gcd(residue * (residue + 2), modulus) == 1:
            residues.append(residue)
            if len(residues) == count:
                break
    return residues


def twin_finite_transcript_composite_lifts() -> dict[str, Any]:
    feature_sets = [
        [6, 10, 14, 15],
        [8, 9, 25],
        [16, 27, 49],
        [32, 81, 125, 49],
    ]
    rows = []
    failures = 0
    total_witnesses = 0
    for moduli in feature_sets:
        transcript_modulus = lcm_many(moduli)
        residues = first_admissible_residues(transcript_modulus, 32)
        q, r = first_primes_above(max(moduli))
        period = transcript_modulus * q * r
        row_failures = 0
        maximum_witness = 0
        examples = []
        for residue in residues:
            witness, crt_modulus = crt(
                [(residue, transcript_modulus), (0, q), ((-2) % r, r)]
            )
            if witness <= q or witness + 2 <= r:
                witness += crt_modulus
            maximum_witness = max(maximum_witness, witness)
            checks = {
                "same_full_transcript": all(witness % modulus == residue % modulus for modulus in moduli),
                "left_proper_composite": witness % q == 0 and witness > q,
                "right_proper_composite": (witness + 2) % r == 0 and witness + 2 > r,
                "below_twice_period": witness < 2 * period,
            }
            row_failures += sum(int(not value) for value in checks.values())
            if len(examples) < 3:
                examples.append(
                    {
                        "admissible_residue": residue,
                        "composite_pair_start": str(witness),
                        "checks": checks,
                    }
                )
        failures += row_failures
        total_witnesses += len(residues)
        rows.append(
            {
                "feature_moduli": moduli,
                "factored_transcript_modulus": transcript_modulus,
                "left_factor_q": q,
                "right_factor_r": r,
                "audited_admissible_residue_count": len(residues),
                "maximum_witness": str(maximum_witness),
                "strict_bound": str(2 * period),
                "examples": examples,
                "row_failure_count": row_failures,
            }
        )
    return {
        "theorem_name": "FiniteCongruenceTranscriptCompositeLift",
        "title_ko": "유한 합동 transcript의 합성수 쌍 lift 정리",
        "declared_target": (
            "Extend the primorial-only TICKET134 obstruction to every finite family "
            "of exact modular features, including overlapping composite moduli."
        ),
        "proved_statement": (
            "Every finite exact congruence transcript n mod m_i factors through one "
            "class a mod L=lcm(m_i). For every locally admissible class "
            "gcd(a(a+2),L)=1 and distinct primes q,r not dividing L, CRT constructs "
            "n with the same transcript, q|n, r|(n+2), and n<2Lqr, with both terms "
            "proper composite. Consequently no locally admissible transcript is a "
            "sufficient certificate of twin primality. If a transcript is also "
            "occupied by a twin-prime pair in the range, no rule using only that "
            "transcript can distinguish the prime and composite realizers."
        ),
        "proved_statement_ko": (
            "유한 개의 정확한 나머지 특성 n mod m_i는 L=lcm(m_i)에 대한 한 "
            "나머지류로 합쳐진다. 모든 국소 허용류에는 같은 transcript를 "
            "가지면서 n과 n+2가 각각 서로 다른 소수 인수를 갖는 합성수 쌍이 "
            "2Lqr 아래에 존재한다. 따라서 어떤 국소 허용 transcript도 쌍둥이 "
            "소수성의 충분조건은 아니다. 같은 transcript에 실제 twin pair도 "
            "있을 때에는 transcript-only 규칙으로 둘을 구별할 수 없다."
        ),
        "proof": (
            "Compatibility of the transcript is equivalent to one residue a modulo "
            "L. Local admissibility makes a and a+2 coprime to L. Choose q,r not "
            "dividing L and apply CRT to n=a mod L, n=0 mod q, n=-2 mod r. The "
            "least nonnegative solution is below Lqr; adding one period only when "
            "needed to make the factors proper gives n<2Lqr without changing any "
            "feature."
        ),
        "finite_transcript_audit": {
            "rows": rows,
            "total_witnesses": total_witnesses,
            "failure_count": failures,
        },
        "route_decision": {
            "retain": "non-congruence Type II correlation or factor-sensitive information at the candidate scale",
            "discard": "every finite exact modular transcript as a sufficient certificate of twin primality",
            "next_theorem": "NonCongruenceTypeIITwinSeparation",
        },
        "machine_audit": {
            "feature_family_count": len(rows),
            "audited_witness_count": total_witnesses,
            "all_transcript_lifts_verified": failures == 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "The theorem refutes transcript admissibility as a sufficient primality "
            "certificate; a classifier impossibility claim additionally requires a "
            "prime and composite realizer in the same transcript. It neither "
            "constructs a Twin Prime counterexample nor proves infinitely many twin "
            "primes. Non-modular analytic correlations remain outside the theorem."
        ),
    }


def build_audit() -> dict[str, Any]:
    sections = {
        "riemann": sharp_block_tail_positivity(),
        "collatz": collatz_full_measure_prefix_cover(),
        "goldbach": goldbach_hard_stratum_moment_bridge(),
        "twin_prime": twin_finite_transcript_composite_lifts(),
    }
    failures = sum(section["machine_audit"]["total_failure_count"] for section in sections.values())
    return {
        "theorem_name": "FourConjectureConditionalBridgeAndExceptionalSetAudit",
        **sections,
        "cross_problem_theorem": {
            "name": "ConditionalBridgeVersusExceptionalSetSeparation",
            "statement": (
                "Each track now has an exact promotion rule and an exact boundary: "
                "a Schur-margin rule whose actual Weil constants are missing; a "
                "full-measure Collatz slope cover that may miss every natural code; "
                "a sparse-stratum norm bridge without an arithmetic residual bound; "
                "and a finite-transcript Twin no-go that leaves nonlocal correlations."
            ),
            "statement_ko": (
                "네 트랙 모두에서 조건부 승격 정리와 그 정리가 넘지 못하는 "
                "예외집합, 상수 또는 정보 경계를 분리했다. 유한 계산은 이 열린 "
                "전제를 대신하지 않는다."
            ),
        },
        "literature_boundary": [
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": "Continuous Weil-form context; no projected block constants are imported.",
            },
            {
                "citation": "Bernstein and Lagarias, The 3x+1 Conjugacy Map",
                "url": "https://doi.org/10.4153/CJM-1996-060-x",
                "role": "2-adic coding context; an almost-everywhere statement is not a theorem about every natural orbit.",
            },
            {
                "citation": "Zhao, The exceptional set of Goldbach problem",
                "url": "https://arxiv.org/abs/2511.05631",
                "role": "Exceptional-set estimates remain distinct from the hard-stratum pointwise residual bound required here.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Modern sieve context; no exact-gap non-congruence separator is imported.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_theorem_count": 4,
            "route_correction_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET135 proves four exact conditional bridge or no-go theorems. None "
            "proves or refutes RH, Collatz, strong Goldbach, or Twin Prime. No finite "
            "audit is promoted to a universal statement, and all four conjecture "
            "resolution counters remain zero. No conjecture proof or conjecture "
            "counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-135",
            "SharpBlockTailPositivityCertificate",
            "ProjectedWeilBlockConstantsWithPositiveSchurMargin",
            "Freeze one Weil normalization and derive outward-rounded alpha, gamma, beta bounds for a growing projected core/tail split.",
        ),
        (
            "collatz",
            "CO-TICKET-135",
            "MinimalNegativeSlopePrefixesFormFullMeasurePrefixFreeCover",
            "NaturalCodesCrossAffineDescentThreshold",
            "Characterize the null exceptional code set and prove that every natural valuation code leaves it while exceeding its affine descent threshold.",
        ),
        (
            "goldbach",
            "GB-TICKET-135",
            "SparseHardStratumMomentToMaximumBridge",
            "BinaryGoldbachHardStratumLogMomentBoundK56",
            "Define the actual minimal-main hard stratum and prove its normalized moment is at most (5/6)m_56 at p=4 ceil(log_2 h).",
        ),
        (
            "twin-prime",
            "TP-TICKET-135",
            "FiniteCongruenceTranscriptCompositeLift",
            "NonCongruenceTypeIITwinSeparation",
            "Construct and certify a factor-sensitive Type II statistic not measurable with respect to any finite congruence transcript, then transfer positivity to gap two.",
        ),
    ]
    attempts = []
    for problem_id, ticket_id, result, target, experiment in specs:
        section_key = problem_id.replace("-", "_")
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": ticket_id,
                "status": "exact_conditional_bridge_or_no_go_conjecture_open",
                "route": result,
                "bounded_result": {"audit_ref": section_key},
                "candidate_theorem": target,
                "next_experiment": experiment,
                "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
                "proof_boundary": audit[section_key]["proof_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "exact_conditional_bridges_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "conditional_bridge_and_exceptional_set_audit": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket135-conditional-bridges-and-exceptional-set.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-135-block-tail-certificate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-135-full-measure-prefix-cover.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-135-hard-stratum-moment-bridge.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-135-congruence-transcript-lifts.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(json.dumps({"schema": SCHEMA, "machine_audit": audit["machine_audit"]}, indent=2))
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
