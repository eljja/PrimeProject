from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "primeproject.ticket233-logarithmic-frame-density-shell-entropy.v1"
GENERATED_AT = "2026-08-21T23:30:00+09:00"
STATUS = "open_not_proven"
AUDIT_KEY = "logarithmic_frame_density_shell_entropy_audit"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def primes_up_to(limit: int) -> tuple[int, ...]:
    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            sieve[prime * prime : limit + 1 : prime] = b"\x00" * (
                (limit - prime * prime) // prime + 1
            )
    return tuple(index for index, flag in enumerate(sieve) if flag)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def next_prime(value: int) -> int:
    candidate = max(2, value)
    while not is_prime(candidate):
        candidate += 1
    return candidate


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {
        "exact": str(value),
        "float": float(value),
    }


def generic_proof_dag(
    prefix: str,
    current: str,
    discarded: str,
    successor: str,
    parent: str,
) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": f"{prefix}-T232", "label": "TICKET232Input", "status": "closed"},
            {"id": f"{prefix}-T233", "label": current, "status": "closed"},
            {
                "id": f"{prefix}-N233",
                "label": discarded,
                "status": "refuted_or_limited",
            },
            {
                "id": f"{prefix}-OPEN233",
                "label": successor,
                "status": "highest_risk_open",
            },
            {"id": prefix, "label": parent, "status": "open_not_proven"},
        ],
        "edges": [
            [f"{prefix}-T232", f"{prefix}-T233"],
            [f"{prefix}-T233", f"{prefix}-N233"],
            [f"{prefix}-T233", f"{prefix}-OPEN233"],
            [f"{prefix}-OPEN233", prefix],
        ],
    }


def riemann_logarithmic_frame_audit() -> dict[str, Any]:
    failures = 0
    rows: list[dict[str, Any]] = []
    for horizon in (16, 64, 256, 1024, 4096):
        modulus = next_prime(horizon + 1)
        dimension = math.ceil(8.0 * math.log(2.0 * horizon))
        rng = random.Random(233_000 + horizon)
        residues = [rng.randrange(modulus) for _ in range(dimension)]
        energies = [
            sum(
                2.0 - 2.0 * math.cos(2.0 * math.pi * frequency * residue / modulus)
                for residue in residues
            )
            / dimension
            for frequency in range(1, horizon + 1)
        ]
        minimum_energy = min(energies)
        minimizing_frequency = energies.index(minimum_energy) + 1
        union_failure_bound = horizon * math.exp(-dimension / 8.0)
        verified = (
            modulus > horizon
            and is_prime(modulus)
            and dimension == math.ceil(8.0 * math.log(2.0 * horizon))
            and union_failure_bound <= 0.5 + 1e-15
            and minimum_energy >= 1.0
        )
        failures += int(not verified)
        rows.append(
            {
                "frequency_horizon_T": horizon,
                "prime_phase_modulus_P": modulus,
                "frame_dimension_M": dimension,
                "phase_residues_mod_P": residues,
                "minimum_normalized_energy": minimum_energy,
                "minimizing_frequency_n": minimizing_frequency,
                "hoeffding_union_failure_bound": union_failure_bound,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For every integer T>=2, every prime P>T, and "
        "M=ceil(8 log(2T)), there exist residues r_1,...,r_M modulo P such "
        "that M^(-1) sum_j |1-exp(-2*pi*i*n*r_j/P)|^2>=1 for every "
        "1<=n<=T. Replacing residue zero by the real phase one and taking "
        "q_j=exp(2*pi*alpha_j)>1 gives a height-adaptive scalar dilation "
        "frame with a uniform unit floor and O(log T) coordinates."
    )
    proof = (
        "Choose the residues independently and uniformly modulo P. For each "
        "fixed 1<=n<=T, multiplication by n permutes the residues because "
        "P>T. Thus X_j=|1-exp(-2*pi*i*n*r_j/P)|^2 lies in [0,4] and has "
        "mean 2. Hoeffding gives P(M^(-1)sum X_j<1)<=exp(-M/8). A union "
        "bound over T frequencies is at most T exp(-M/8)<=1/2, so a common "
        "frame exists. Rational representatives give q_j>1. Together with "
        "TICKET-232, the scalar effective-dimension threshold is Theta(log T)."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "deterministic_seeded_frame_rows": rows,
        "aggregate": {
            "logarithmic_scalar_adaptive_frame_exists": True,
            "ticket232_logarithmic_lower_bound_sharp_for_scalar_energy": True,
            "superlogarithmic_scalar_dimension_necessity_refuted": True,
            "actual_weil_quadratic_form_transfer_proved": False,
            "explicit_signed_weil_tail_dominance_proved": False,
            "riemann_hypothesis_resolved": False,
        },
        "no_go_scope": (
            "The construction refutes any superlogarithmic dimension necessity "
            "for the scalar phase-energy problem. It does not transfer the "
            "floor to the signed Guinand-Weil quadratic form or dominate its "
            "arithmetic tail. The seeded rows witness the construction but the "
            "existence theorem comes from Hoeffding and the union bound."
        ),
        "failure_count": failures,
    }


def rotate_left(word: tuple[int, ...], amount: int) -> tuple[int, ...]:
    amount %= len(word)
    return word[amount:] + word[:amount]


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(rotate_left(word, amount) for amount in range(len(word)))


def is_primitive_word(word: tuple[int, ...]) -> bool:
    height = len(word)
    for period in range(1, height):
        if height % period == 0 and word == word[:period] * (height // period):
            return False
    return True


def collatz_denominator(word: tuple[int, ...]) -> int:
    return 2 ** sum(word) - 3 ** len(word)


def collatz_numerator(word: tuple[int, ...]) -> int:
    prefix = 0
    numerator = 0
    height = len(word)
    for index, valuation in enumerate(word):
        numerator += 3 ** (height - index - 1) * 2**prefix
        prefix += valuation
    return numerator


def mobius(value: int) -> int:
    if value == 1:
        return 1
    remaining = value
    factors = 0
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            factors += 1
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        factors += 1
    return -1 if factors % 2 else 1


def divisors(value: int) -> list[int]:
    result = []
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            result.append(divisor)
            if divisor * divisor != value:
                result.append(value // divisor)
    return sorted(result)


def primitive_binary_necklace_count(height: int, one_count: int) -> int:
    total = 0
    for divisor in divisors(math.gcd(height, one_count)):
        total += mobius(divisor) * math.comb(height // divisor, one_count // divisor)
    return total // height


def load_json(relative_path: str) -> dict[str, Any]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def collatz_arbitrary_tail_lineage_rows() -> tuple[list[dict[str, Any]], int]:
    paths = {
        1: "data/open-problem/collatz/co-ticket-206-single-one-general.json",
        2: "data/open-problem/collatz/co-ticket-207-two-one-general.json",
        3: "data/open-problem/collatz/co-ticket-208-three-one-exclusion.json",
        4: "data/open-problem/collatz/co-ticket-209-four-one-exclusion.json",
        5: "data/open-problem/collatz/co-ticket-210-five-one-general.json",
        6: "data/open-problem/collatz/co-ticket-213-six-one-exclusion.json",
        7: "data/open-problem/collatz/co-ticket-214-seven-one-exclusion.json",
    }
    flag_names = {
        1: "single_one_arbitrary_ge_two_cycle_stratum_excluded",
        2: "exactly_two_valuation_one_cycle_stratum_excluded",
        3: "exactly_three_valuation_one_cycle_stratum_excluded",
        4: "exactly_four_valuation_one_cycle_stratum_excluded",
        5: "exactly_five_valuation_one_cycle_stratum_excluded",
        6: "exactly_six_valuation_one_cycle_stratum_excluded",
        7: "exactly_seven_valuation_one_cycle_stratum_excluded",
    }
    rows = []
    failures = 0
    for one_count, relative_path in paths.items():
        payload = load_json(relative_path)
        computation = payload.get("reproducible_computation", {})
        aggregate = computation.get("aggregate", {})
        closed = aggregate.get(flag_names[one_count]) is True
        failure_count = computation.get("failure_count", 0)
        failures += int(not closed or failure_count != 0)
        rows.append(
            {
                "valuation_one_count_k": one_count,
                "source_ticket_id": payload.get("ticket_id", f"CO-TICKET-{205+one_count}"),
                "source_path": relative_path,
                "closure_flag": flag_names[one_count],
                "stratum_closed": closed,
                "exact_words_enumerated": computation.get("total_exact_words_enumerated"),
                "source_failure_count": failure_count,
            }
        )
    return rows, failures


def collatz_binary_lineage_rows() -> tuple[list[dict[str, Any]], int]:
    paths = {
        4: "data/open-problem/collatz/co-ticket-188-four-one-cycle-exclusion.json",
        5: "data/open-problem/collatz/co-ticket-189-five-one-cycle-exclusion.json",
        6: "data/open-problem/collatz/co-ticket-190-six-one-cycle-exclusion.json",
        7: "data/open-problem/collatz/co-ticket-191-seven-one-cycle-exclusion.json",
        8: "data/open-problem/collatz/co-ticket-192-eight-one-cycle-exclusion.json",
        9: "data/open-problem/collatz/co-ticket-193-nine-one-cycle-exclusion.json",
        10: "data/open-problem/collatz/co-ticket-194-ten-one-cycle-exclusion.json",
        11: "data/open-problem/collatz/co-ticket-195-eleven-one-decidability.json",
    }
    rows = []
    failures = 0
    for one_count, relative_path in paths.items():
        payload = load_json(relative_path)
        computation = payload["reproducible_computation"]
        aggregate = computation["aggregate"]
        closed = (
            aggregate.get("infinite_family_proved") is True
            if one_count <= 10
            else aggregate.get("eleven_one_infinite_family_proved_empty") is True
        )
        represented = int(aggregate["finite_exception_word_count"])
        hits = int(aggregate["divisibility_hits"])
        source_failures = int(computation["failure_count"])
        failures += int(not closed or hits != 0 or source_failures != 0)
        rows.append(
            {
                "valuation_one_count_k": one_count,
                "source_ticket_id": payload["ticket_id"],
                "source_path": relative_path,
                "stratum_closed": closed,
                "finite_normalized_words_represented": represented,
                "divisibility_hits": hits,
                "source_failure_count": source_failures,
            }
        )
    return rows, failures


def boundary_components(
    one_count: int, horizon: int
) -> tuple[int, list[list[int]]]:
    if horizon < one_count:
        raise ValueError("horizon must contain every valuation-one position")
    prefixes: list[list[int]] = []
    for ones_before in range(one_count + 1):
        values = [0]
        running = 0
        for index in range(horizon):
            exponent = 2 * index - ones_before
            if exponent >= 0:
                running += 3 ** (horizon - 1 - index) * 2**exponent
            values.append(running)
        prefixes.append(values)
    constant = 3 ** (horizon - 1) + prefixes[one_count][horizon] - prefixes[1][1]
    boundaries = [[0] * horizon for _ in range(one_count)]
    for boundary_index in range(1, one_count):
        for position in range(1, horizon):
            boundaries[boundary_index][position] = (
                prefixes[boundary_index][position + 1]
                - prefixes[boundary_index + 1][position + 1]
            )
    return constant, boundaries


def boundary_numerator(
    one_count: int, horizon: int, positions: tuple[int, ...]
) -> int:
    if len(positions) != one_count or positions[0] != 0:
        raise ValueError("positions must be normalized with p_0=0")
    if tuple(sorted(positions)) != positions or positions[-1] >= horizon:
        raise ValueError("positions must be strictly increasing inside the horizon")
    constant, boundaries = boundary_components(one_count, horizon)
    return constant + sum(
        boundaries[index][positions[index]] for index in range(1, one_count)
    )


def direct_numerator_from_positions(horizon: int, positions: tuple[int, ...]) -> int:
    position_set = set(positions)
    word = tuple(1 if index in position_set else 2 for index in range(horizon))
    return collatz_numerator(word)


def twelve_one_boundary_validation() -> dict[str, Any]:
    exhaustive_checked = 0
    exhaustive_mismatches = 0
    exhaustive_transcript = hashlib.sha256()
    for horizon in range(12, 19):
        for tail in itertools.combinations(range(1, horizon), 11):
            positions = (0,) + tail
            direct = direct_numerator_from_positions(horizon, positions)
            separated = boundary_numerator(12, horizon, positions)
            exhaustive_mismatches += int(direct != separated)
            exhaustive_checked += 1
            exhaustive_transcript.update(
                f"{horizon}:{positions}:{direct}:{separated}\n".encode("ascii")
            )

    seeded_checked = 0
    seeded_mismatches = 0
    seeded_transcript = hashlib.sha256()
    for horizon in range(29, 46):
        rng = random.Random(233_012 + horizon)
        for _ in range(128):
            positions = (0,) + tuple(sorted(rng.sample(range(1, horizon), 11)))
            direct = direct_numerator_from_positions(horizon, positions)
            separated = boundary_numerator(12, horizon, positions)
            seeded_mismatches += int(direct != separated)
            seeded_checked += 1
            seeded_transcript.update(
                f"{horizon}:{positions}:{direct}:{separated}\n".encode("ascii")
            )
    return {
        "exact_formula": "B=C_h+sum_{i=1}^{11} E_{i,h}(p_i)",
        "exhaustive_horizons": [12, 18],
        "exhaustive_normalized_words_checked": exhaustive_checked,
        "exhaustive_formula_mismatch_count": exhaustive_mismatches,
        "exhaustive_transcript_sha256": exhaustive_transcript.hexdigest(),
        "seeded_finite_horizon_range": [29, 45],
        "seeded_samples_checked": seeded_checked,
        "seeded_formula_mismatch_count": seeded_mismatches,
        "seeded_transcript_sha256": seeded_transcript.hexdigest(),
    }


def finite_twelve_one_horizon_row(horizon: int) -> dict[str, Any]:
    if not 29 <= horizon <= 45:
        raise ValueError("finite twelve-one decision range is h=29..45")
    denominator = 2 ** (2 * horizon - 12) - 3**horizon
    constant, boundary = boundary_components(12, horizon)
    left_buckets: list[list[tuple[int, tuple[int, ...]]]] = [
        [] for _ in range(horizon)
    ]
    left_tuple_count = 0
    for positions in itertools.combinations(range(1, horizon), 5):
        remainder = (
            constant
            + sum(boundary[index][positions[index - 1]] for index in range(1, 6))
        ) % denominator
        left_buckets[positions[-1]].append((remainder, positions))
        left_tuple_count += 1

    active: dict[int, tuple[int, ...]] = {}
    next_last = 0
    right_tuple_count = 0
    represented_word_count = 0
    hits: list[dict[str, Any]] = []
    transcript = hashlib.sha256()
    for first_right in range(6, horizon - 5):
        while next_last < first_right:
            for remainder, positions in left_buckets[next_last]:
                active.setdefault(remainder, positions)
            next_last += 1
        for tail in itertools.combinations(range(first_right + 1, horizon), 5):
            right_positions = (first_right,) + tail
            right_remainder = sum(
                boundary[index][right_positions[index - 6]]
                for index in range(6, 12)
            ) % denominator
            target = (-right_remainder) % denominator
            hit = target in active
            transcript.update(
                (
                    f"{first_right}:{','.join(map(str, tail))}:"
                    f"{target}:{int(hit)}\n"
                ).encode("ascii")
            )
            if hit:
                hits.append(
                    {
                        "positions": [0, *active[target], *right_positions],
                        "target_remainder": target,
                    }
                )
            right_tuple_count += 1
            represented_word_count += math.comb(first_right - 1, 5)
    expected = math.comb(horizon - 1, 11)
    verified = (
        denominator > 0
        and represented_word_count == expected
        and not hits
    )
    return {
        "horizon_h": horizon,
        "denominator_D": denominator,
        "split": "5+6 boundary terms",
        "left_tuple_count": left_tuple_count,
        "right_tuple_count": right_tuple_count,
        "represented_normalized_word_count": represented_word_count,
        "expected_normalized_word_count": expected,
        "coverage_matches_binomial_count": represented_word_count == expected,
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "mitm_transcript_sha256": transcript.hexdigest(),
        "certificate_verified": verified,
    }


def collatz_density_band_audit() -> dict[str, Any]:
    failures = 0
    arbitrary_lineage_rows, arbitrary_lineage_failures = (
        collatz_arbitrary_tail_lineage_rows()
    )
    binary_lineage_rows, binary_lineage_failures = collatz_binary_lineage_rows()
    failures += arbitrary_lineage_failures + binary_lineage_failures
    scan_rows: list[dict[str, Any]] = []
    total_raw = 0
    total_primitive = 0
    total_hits = 0
    for height in range(3, 23):
        admissible_counts = [
            one_count
            for one_count in range(1, height)
            if 6**height <= 5**height * 2**one_count
            and 2 ** (2 * height - one_count) > 3**height
        ]
        raw_count = sum(math.comb(height, one_count) for one_count in admissible_counts)
        necklaces: set[tuple[int, ...]] = set()
        for one_count in admissible_counts:
            for positions in itertools.combinations(range(height), one_count):
                word_list = [2] * height
                for position in positions:
                    word_list[position] = 1
                necklaces.add(canonical_rotation(tuple(word_list)))
        primitive = sorted(word for word in necklaces if is_primitive_word(word))
        formula_count = sum(
            primitive_binary_necklace_count(height, one_count)
            for one_count in admissible_counts
        )
        transcript = hashlib.sha256()
        hits = []
        for word in primitive:
            denominator = collatz_denominator(word)
            numerator = collatz_numerator(word)
            remainder = numerator % denominator
            transcript.update(
                ("".join(map(str, word)) + ":" + str(remainder) + "\n").encode("ascii")
            )
            if remainder == 0:
                hits.append("".join(map(str, word)))
        verified = (
            len(primitive) == formula_count
            and not hits
            and all(collatz_denominator(word) > 0 for word in primitive)
        )
        failures += int(not verified)
        total_raw += raw_count
        total_primitive += len(primitive)
        total_hits += len(hits)
        scan_rows.append(
            {
                "height_h": height,
                "admissible_one_counts_k": admissible_counts,
                "raw_binary_word_count": raw_count,
                "primitive_necklace_count": len(primitive),
                "mobius_formula_primitive_count": formula_count,
                "divisibility_hit_count": len(hits),
                "transcript_sha256": transcript.hexdigest(),
                "certificate_verified": verified,
            }
        )

    unbounded_rows = []
    for multiplier in (1, 2, 3, 5, 11, 31):
        height = 3 * multiplier
        one_count = multiplier
        word = (1,) * multiplier + (2,) * (2 * multiplier)
        verified = (
            is_primitive_word(word)
            and 6**height <= 5**height * 2**one_count
            and 2 ** (2 * height - one_count) > 3**height
        )
        failures += int(not verified)
        unbounded_rows.append(
            {
                "multiplier_m": multiplier,
                "height_h": height,
                "one_count_k": one_count,
                "density_k_over_h": str(Fraction(one_count, height)),
                "primitive": is_primitive_word(word),
                "density_floor_integer_inequality": 6**height <= 5**height * 2**one_count,
                "positive_denominator_integer_inequality": 2 ** (2 * height - one_count) > 3**height,
                "certificate_verified": verified,
            }
        )

    prime_necklace_rows = []
    for prime_k in (2, 3, 5, 7, 11, 13, 17, 19):
        height = 3 * prime_k
        formula = (math.comb(height, prime_k) - 3) // height
        independent = primitive_binary_necklace_count(height, prime_k)
        verified = formula == independent and formula > 0
        failures += int(not verified)
        prime_necklace_rows.append(
            {
                "prime_one_count_k": prime_k,
                "height_3k": height,
                "primitive_necklaces_exact": formula,
                "formula": "(binom(3k,k)-3)/(3k)",
                "mobius_formula_verified": verified,
            }
        )

    twelve_validation = twelve_one_boundary_validation()
    failures += int(twelve_validation["exhaustive_formula_mismatch_count"] != 0)
    failures += int(twelve_validation["seeded_formula_mismatch_count"] != 0)
    twelve_rows = [finite_twelve_one_horizon_row(horizon) for horizon in range(29, 46)]
    failures += sum(int(not row["certificate_verified"]) for row in twelve_rows)
    twelve_represented = sum(
        int(row["represented_normalized_word_count"]) for row in twelve_rows
    )
    twelve_expected = math.comb(45, 12) - math.comb(28, 12)
    twelve_hits = sum(int(row["divisibility_hit_count"]) for row in twelve_rows)
    twelve_left = sum(int(row["left_tuple_count"]) for row in twelve_rows)
    twelve_right = sum(int(row["right_tuple_count"]) for row in twelve_rows)
    density_at_45 = Fraction(2**12) * Fraction(5, 6) ** 45
    density_at_46 = Fraction(2**12) * Fraction(5, 6) ** 46
    failures += int(twelve_represented != twelve_expected)
    failures += int(twelve_hits != 0)
    failures += int(2 ** (2 * 28 - 12) > 3**28)
    failures += int(2 ** (2 * 29 - 12) <= 3**29)
    failures += int(density_at_45 < 1 or density_at_46 >= 1)

    theorem = (
        "The CO-OPEN232 target BinaryFourOneCriticalStripNondivisibility was "
        "already closed by TICKET-188 and is a special case of the stronger "
        "TICKET-209 arbitrary-tail four-one exclusion; binary multiplicities "
        "four through eleven were already closed by TICKETS 188-195. The "
        "first open binary stratum, exactly twelve valuation ones and all "
        "other valuations two, is now excluded as a positive cycle: contraction "
        "starts at h=29, the product bound excludes h>=46, and an exact 5+6 "
        "meet-in-the-middle residue computation excludes every h=29,...,45, "
        "representing 28,729,599,990 first-one-normalized words without a hit. "
        "Thus a hypothetical binary cycle is primitive, has k>=13, and obeys "
        "log2(6/5)<=k/h<2-log2(3); a general valuation cycle has k>=8. The "
        "primitive words 1^m 2^(2m) show that every finite fixed-k ladder is "
        "noncofinal, and for prime k the h=3k slice has exactly "
        "(binom(3k,k)-3)/(3k) primitive necklaces."
    )
    proof = (
        "TICKET-182 proves that D>0 and D|B are equivalent to realization of "
        "the corresponding positive accelerated cycle. The prior machine "
        "artifacts close every arbitrary-tail multiplicity "
        "k<=7 and every binary multiplicity k<=11, so TICKET-232's successor "
        "was not open. For k=12, normalize a one to p_0=0. Telescoping the "
        "prefix-one step function gives B=C_h+sum_(i=1)^11 E_(i,h)(p_i). "
        "Split the eleven free positions into 5+6 boundary terms, activate "
        "left residues precisely when p_5<p_6, and match the complementary "
        "right residue modulo D. Vandermonde's identity gives complete "
        "coverage C(h-1,11). The scalar gates leave exactly h=29,...,45, and "
        "the exact MITM finds no residue zero. TICKET-211 also gives "
        "6^h<=5^h 2^k for every positive integer cycle. For a binary word, "
        "S=2h-k and D>0 is exactly 2^(2h-k)>3^h, giving the upper density "
        "edge. A nontrivial repeated cycle reduces to a primitive root. The "
        "word 1^m2^(2m) has one cyclic run of each symbol and is primitive; "
        "216<250 and 27<32 prove both band inequalities after taking the "
        "m-th power. The weighted primitive-necklace formula is Mobius "
        "inversion; for prime k and h=3k it reduces to the displayed count."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "arbitrary_tail_closed_multiplicity_lineage_rows": arbitrary_lineage_rows,
        "binary_closed_multiplicity_lineage_rows": binary_lineage_rows,
        "twelve_one_boundary_validation": twelve_validation,
        "twelve_one_finite_horizon_rows": twelve_rows,
        "twelve_one_finite_horizon_totals": {
            "contracting_range_starts_at_h": 29,
            "product_bound_analytic_exclusion_starts_at_h": 46,
            "finite_exact_horizons": [29, 45],
            "left_tuple_count": twelve_left,
            "right_tuple_count": twelve_right,
            "represented_normalized_words": twelve_represented,
            "expected_normalized_words": twelve_expected,
            "divisibility_hits": twelve_hits,
            "product_bound_at_h45": fraction_payload(density_at_45),
            "product_bound_at_h46": fraction_payload(density_at_46),
        },
        "finite_density_band_scan_rows": scan_rows,
        "finite_density_band_scan_totals": {
            "raw_binary_words": total_raw,
            "primitive_necklaces": total_primitive,
            "divisibility_hits": total_hits,
            "maximum_height_h": 22,
            "regression_only": True,
        },
        "unbounded_primitive_band_family_rows": unbounded_rows,
        "prime_weight_primitive_necklace_growth_rows": prime_necklace_rows,
        "aggregate": {
            "ticket232_four_one_successor_already_closed": True,
            "ticket232_one_through_three_result_already_subsumed": True,
            "arbitrary_tail_multiplicity_one_through_seven_closed": True,
            "binary_multiplicity_four_through_eleven_already_closed": True,
            "binary_exactly_twelve_positive_cycle_stratum_excluded": True,
            "binary_remaining_multiplicity_lower_bound_k": 13,
            "general_remaining_multiplicity_lower_bound_k": 8,
            "binary_cycle_density_band_proved": True,
            "finite_fixed_multiplicity_ladder_noncofinal": True,
            "all_unbounded_multiplicities_excluded": False,
            "aperiodic_descent_proved": False,
            "collatz_conjecture_resolved": False,
        },
        "no_go_scope": (
            "This corrects a proof-DAG regression, closes the first genuinely "
            "open binary fixed stratum k=12, and proves that iterating fixed-k "
            "enumeration cannot be cofinal. The height-22 density scan is only "
            "a regression audit. The k=12 computation is exhaustive only "
            "because independent scalar gates prove that h=29,...,45 is the "
            "entire finite decision range. Uniform k>=13 binary necklaces, "
            "valuations at least three, and aperiodic descent remain open."
        ),
        "failure_count": failures,
    }


def euler_phi(value: int) -> int:
    result = value
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            while remaining % prime == 0:
                remaining //= prime
            result -= result // prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def is_squarefree(value: int) -> bool:
    for prime in range(2, math.isqrt(value) + 1):
        if value % (prime * prime) == 0:
            return False
    return True


def ramanujan_sum(modulus: int, target: int) -> int:
    common = math.gcd(modulus, target)
    return sum(
        divisor * mobius(modulus // divisor)
        for divisor in divisors(common)
    )


def goldbach_squarefree_row(limit: int, modulus: int, target: int) -> dict[str, Any]:
    units = [residue for residue in range(modulus) if math.gcd(residue, modulus) == 1]
    masses = {residue: 0 for residue in units}
    for prime in primes_up_to(limit):
        if math.gcd(prime, modulus) == 1:
            masses[prime % modulus] += 1
    phi = len(units)
    total = sum(masses.values())
    mean = Fraction(total, phi)
    epsilon = max(abs(Fraction(masses[residue]) - mean) for residue in units) / mean
    shell = sum(
        masses[left] * masses[right] * ramanujan_sum(modulus, left + right - target)
        for left in units
        for right in units
    )
    base = mean * mean * ramanujan_sum(modulus, target)
    correction = Fraction(shell) - base
    bound = mean * mean * (
        2 * phi * phi * epsilon + phi**3 * epsilon * epsilon
    )
    verified = (
        modulus % 2 == 1
        and is_squarefree(modulus)
        and abs(correction) <= bound
        and ramanujan_sum(modulus, target) != 0
    )
    return {
        "prime_limit_X": limit,
        "odd_squarefree_modulus_q": modulus,
        "target_N": target,
        "phi_q": phi,
        "prime_indicator_total_W": total,
        "maximum_relative_residue_discrepancy_epsilon": fraction_payload(epsilon),
        "exact_shell_T": shell,
        "uniform_ramanujan_base": fraction_payload(base),
        "exact_correction": fraction_payload(correction),
        "deterministic_error_bound": fraction_payload(bound),
        "certificate_verified": verified,
    }


def prime_parseval_row(limit: int, prime_l: int) -> dict[str, Any]:
    masses = [0] * prime_l
    for prime in primes_up_to(limit):
        if prime != prime_l:
            masses[prime % prime_l] += 1
    total = sum(masses)
    mean = Fraction(total, prime_l - 1)
    corrections: list[Fraction] = []
    for target in range(prime_l):
        congruent_pairs = sum(
            masses[left] * masses[(target - left) % prime_l]
            for left in range(1, prime_l)
            if (target - left) % prime_l != 0
        )
        shell = prime_l * congruent_pairs - total * total
        base = (
            Fraction(total * total, prime_l - 1)
            if target == 0
            else Fraction(-total * total, (prime_l - 1) ** 2)
        )
        corrections.append(Fraction(shell) - base)
    target_energy = sum(value * value for value in corrections)
    spectral_energy = 0.0
    for frequency in range(1, prime_l):
        exponential_sum = sum(
            masses[residue] * cmath.exp(2j * math.pi * frequency * residue / prime_l)
            for residue in range(1, prime_l)
        )
        spectral_energy += abs(exponential_sum**2 - float(mean * mean)) ** 2
    parseval_error = abs(float(target_energy) - prime_l * spectral_energy)
    verified = parseval_error <= 1e-7 * max(1.0, float(target_energy))
    return {
        "prime_limit_X": limit,
        "prime_modulus_l": prime_l,
        "prime_indicator_total_W": total,
        "target_correction_energy_exact": str(target_energy),
        "target_correction_energy_float": float(target_energy),
        "spectral_energy_float": spectral_energy,
        "parseval_scaled_spectral_energy_float": prime_l * spectral_energy,
        "absolute_parseval_error": parseval_error,
        "parseval_identity_verified": verified,
    }


def goldbach_sparse_row(limit: int) -> dict[str, Any]:
    prime_l = next_prime(2 * limit + 2)
    target_residue = 2 * limit + 1
    target = prime_l + target_residue
    primes = primes_up_to(limit)
    total = len(primes)
    congruent_pairs = sum(
        1
        for left in primes
        for right in primes
        if (left + right - target_residue) % prime_l == 0
    )
    shell = prime_l * congruent_pairs - total * total
    base = Fraction(-total * total, (prime_l - 1) ** 2)
    mean_square = Fraction(total * total, (prime_l - 1) ** 2)
    ratio = abs(Fraction(shell) - base) / mean_square
    expected_ratio = prime_l * (prime_l - 2)
    verified = (
        target % 2 == 0
        and prime_l > 2 * limit + 1
        and congruent_pairs == 0
        and shell == -(total * total)
        and ratio == expected_ratio
    )
    return {
        "prime_limit_X": limit,
        "sparse_prime_modulus_l": prime_l,
        "even_target_N": target,
        "target_residue_n": target_residue,
        "prime_count_W": total,
        "congruent_pair_count": congruent_pairs,
        "exact_shell_T": shell,
        "uniform_singular_base": str(base),
        "correction_to_mu_squared_ratio": str(ratio),
        "expected_ratio_l_times_l_minus_2": expected_ratio,
        "certificate_verified": verified,
    }


def goldbach_shell_audit() -> dict[str, Any]:
    failures = 0
    squarefree_rows = [
        goldbach_squarefree_row(limit, modulus, target)
        for limit, modulus, target in (
            (1_000, 15, 666),
            (3_000, 21, 2_000),
            (10_000, 35, 6_666),
            (30_000, 105, 20_000),
        )
    ]
    parseval_rows = [
        prime_parseval_row(limit, prime_l)
        for limit, prime_l in ((100, 5), (300, 7), (1_000, 11), (3_000, 13))
    ]
    sparse_rows = [goldbach_sparse_row(limit) for limit in (10, 100, 1_000, 10_000)]
    failures += sum(int(not row["certificate_verified"]) for row in squarefree_rows)
    failures += sum(int(not row["parseval_identity_verified"]) for row in parseval_rows)
    failures += sum(int(not row["certificate_verified"]) for row in sparse_rows)

    theorem = (
        "For every odd squarefree q and nonnegative residue masses with mean "
        "mu and maximum relative discrepancy epsilon, the reduced rational "
        "shell satisfies T_q(N)=mu^2 c_q(N)+R_q(N), with "
        "|R_q(N)|<=mu^2(2 phi(q)^2 epsilon+phi(q)^3 epsilon^2). "
        "Siegel-Walfisz therefore gives, for log-prime weights, uniformly for "
        "q<=(log X)^B and every N, T_(q,X)(N)=mu^2 c_q(N)+o_B(mu^2). "
        "For prime l the correction also obeys the exact Parseval identity. "
        "Without any q-X-N coupling, actual primes with l>2X+1 give a sparse "
        "cutoff family whose relative shell correction is l(l-2)."
    )
    proof = (
        "For a unit a and squarefree q, c_q(a)=Mobius(q). Writing the residue "
        "Fourier sum as mu*Mobius(q)+D_a gives |D_a|<=phi(q)epsilon mu; "
        "squaring and summing over phi(q) unit frequencies proves the bound. "
        "Siegel-Walfisz makes epsilon=O_B(q exp(-c_B sqrt(log X))), so the "
        "bound is o_B(mu^2) throughout the polylogarithmic squarefree range. "
        "Squarefree Ramanujan sums never vanish. Fourier Parseval gives "
        "sum_n|R_l(n)|^2=l sum_(a!=0)|S(a/l)^2-mu^2|^2. Finally, if "
        "l>2X+1 and N=l+2X+1, no pair p_1,p_2<=X reaches the target residue; "
        "the TICKET-232 identity gives T=-W^2 and the exact divergent ratio."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "squarefree_indicator_algebra_rows": squarefree_rows,
        "prime_modulus_parseval_rows": parseval_rows,
        "actual_prime_sparse_denominator_no_go_rows": sparse_rows,
        "siegel_walfisz_input": {
            "weight": "omega_p=log(p) for p<=X and gcd(p,q)=1",
            "range": "odd squarefree q<=(log X)^B for fixed B",
            "relative_discrepancy": "epsilon=O_B(q exp(-c_B sqrt(log X)))",
            "consequence": "uniform_N |R_q(N)|/mu^2=o_B(1)",
            "effective_starting_point_provided": False,
        },
        "aggregate": {
            "squarefree_shell_deterministic_error_bound_proved": True,
            "polylogarithmic_squarefree_prime_shell_asymptotic_proved": True,
            "prime_shell_parseval_identity_proved": True,
            "unrestricted_growing_denominator_actual_prime_asymptotic_refuted": True,
            "energy_o_mu4_implies_uniform_target_control": False,
            "minor_arc_negative_mass_controlled": False,
            "strong_goldbach_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The sparse family refutes only an uncoupled denominator-cutoff-target "
            "claim and uses X<N/2, so it is not a Goldbach counterexample. "
            "Siegel-Walfisz is ineffective and treats rational centers only. "
            "Arc neighborhoods, minor arcs, and an every-even-target positive "
            "lower bound remain open. Finite rows audit algebra, not asymptotics."
        ),
        "failure_count": failures,
    }


def twin_entropy_audit() -> dict[str, Any]:
    failures = 0
    primes = [prime for prime in primes_up_to(200) if prime >= 5]
    rows = []
    q_tilt = Fraction(1, 2)
    for dimension in (4, 8, 16, 32):
        active = primes[:dimension]
        damping = Fraction(1, dimension)
        coefficient_norm = (1 + damping) ** dimension - 1
        energy_cap = Fraction(1)
        for prime in active:
            energy_cap *= 1 + Fraction(prime - 1, prime - 3) * damping
        energy_cap -= 1
        mixture_energy = (
            (1 + q_tilt * q_tilt * damping) ** dimension
            + (1 - q_tilt * q_tilt * damping) ** dimension
        ) / 2 - 1
        mixture_signed = (
            (1 + q_tilt * damping) ** dimension
            + (1 - q_tilt * damping) ** dimension
        ) / 2 - 1
        signed_bound_squared = coefficient_norm * mixture_energy
        verified = (
            mixture_energy <= energy_cap
            and mixture_signed * mixture_signed <= signed_bound_squared
            and mixture_signed > 0
        )
        failures += int(not verified)
        rows.append(
            {
                "active_prime_count_m": dimension,
                "active_primes": active,
                "critical_product_damping_x": str(damping),
                "coefficient_norm_R": fraction_payload(coefficient_norm),
                "universal_energy_cap": fraction_payload(energy_cap),
                "even_mixture_damped_energy": fraction_payload(mixture_energy),
                "signed_cauchy_bound_squared": fraction_payload(signed_bound_squared),
                "centered_even_mixture_signed_aggregate": fraction_payload(mixture_signed),
                "certificate_verified": verified,
            }
        )

    parity_rows = []
    eta = 0.25
    for dimension in (4, 8, 16, 32):
        entropy_lower = dimension * eta ** (1.0 / dimension)
        norm_lower = 2**dimension * math.sqrt(eta) - 1.0
        verified = entropy_lower > 0 and norm_lower == 2 ** (dimension - 1) - 1
        failures += int(not verified)
        parity_rows.append(
            {
                "active_prime_count_m": dimension,
                "required_full_mode_multiplier_eta": eta,
                "entropy_sum_lower_bound": entropy_lower,
                "coefficient_norm_lower_bound": norm_lower,
                "certificate_verified": verified,
            }
        )

    theorem = (
        "For normalized centered quadratic CRT signs and any probability "
        "measure, product damping x_S=product_(l in S)x_l satisfies "
        "D_x=sum_(S nonempty)x_S b_S^2<=product_l(1+c_l x_l)-1, where "
        "c_l=(l-1)/(l-3)<=2. Every signed aggregate is bounded in square by "
        "[product(1+x_l)-1][product(1+c_l x_l)-1]. Thus sum x_l=o(1) "
        "forces universal saving. At critical damping x_l=tau/m, however, a "
        "nonnegative even product-tilt mixture has every singleton and odd "
        "coefficient zero while its signed aggregate tends to cosh(tau/2)-1. "
        "If the full-mode multiplier stays at least eta>0, the entropy is at "
        "least m eta^(1/m) and the coefficient norm at least 2^m sqrt(eta)-1."
    )
    proof = (
        "The two squared values of psi_l are (l-3)/(l-1) and "
        "(l-1)/(l-3). Jensen bounds b_S^2 by E_nu psi_S^2; expanding the "
        "product gives the energy cap, and Cauchy gives the signed cap. For "
        "q=1/2, the density one-half times product(1+q psi_l) plus one-half "
        "times product(1-q psi_l) is nonnegative and normalized. Its b_S is "
        "q^|S| in even degree and zero in odd degree, proving the critical "
        "counterfamily. AM-GM gives the entropy lower bound under full-mode "
        "retention, while 1+x>=2 sqrt(x) gives the exponential norm lower bound."
    )
    return {
        "theorem": theorem,
        "proof": proof,
        "critical_entropy_exact_rows": rows,
        "full_parity_retention_no_go_rows": parity_rows,
        "aggregate": {
            "damped_energy_product_cap_proved": True,
            "signed_product_damping_large_sieve_bound_proved": True,
            "vanishing_entropy_universal_signed_saving_proved": True,
            "critical_entropy_plus_centered_marginals_saving_refuted": True,
            "bounded_entropy_product_damping_full_parity_retention_refuted": True,
            "prime_weighted_critical_noise_decay_proved": False,
            "positive_twin_main_term_proved": False,
            "twin_prime_conjecture_resolved": False,
        },
        "no_go_scope": (
            "The counterfamily is a nonnegative CRT probability model, not "
            "actual prime weights. The theorem closes only product damping "
            "based on entropy and local centering. Nonproduct kernels, genuine "
            "prime-weighted Type-II cancellation, a parity-retaining transfer, "
            "and positive twin principal mass remain open."
        ),
        "failure_count": failures,
    }


def collatz_proof_dag() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "CO-T182", "label": "AcceleratedCycleIffAffineDivisibility", "status": "closed"},
            {"id": "CO-T188", "label": "BinaryFourOneCycleExclusion", "status": "closed"},
            {"id": "CO-T209", "label": "ArbitraryTailFourOneCycleExclusion", "status": "closed"},
            {"id": "CO-T195", "label": "BinaryElevenOneCycleExclusion", "status": "closed"},
            {"id": "CO-T214", "label": "ArbitraryTailSevenOneExclusion", "status": "closed"},
            {"id": "CO-N232", "label": "TreatBinaryFourOneAsNewOpenTarget", "status": "refuted_or_limited"},
            {"id": "CO-T233", "label": "BinaryLineageCorrectionTwelveOneExclusionAndFixedStratumNoGo", "status": "closed"},
            {"id": "CO-N233", "label": "FiniteFixedMultiplicityLadderIsCofinal", "status": "refuted_or_limited"},
            {"id": "CO-OPEN233", "label": "UniformBinaryDensityBandPrimitiveNecklaceNondivisibility", "status": "highest_risk_open"},
            {"id": "CO-PERIODIC", "label": "AllPeriodicValuationWordsIncludingValuesAtLeastThree", "status": "open_not_proven"},
            {"id": "CO-APERIODIC", "label": "AperiodicDescentOrTermination", "status": "open_not_proven"},
            {"id": "CO", "label": "CollatzConjecture", "status": "open_not_proven"},
        ],
        "edges": [
            ["CO-T182", "CO-N232"],
            ["CO-T182", "CO-T233"],
            ["CO-T188", "CO-N232"],
            ["CO-T209", "CO-N232"],
            ["CO-T195", "CO-T233"],
            ["CO-T214", "CO-T233"],
            ["CO-N232", "CO-T233"],
            ["CO-T233", "CO-N233"],
            ["CO-T233", "CO-OPEN233"],
            ["CO-OPEN233", "CO-PERIODIC"],
            ["CO-PERIODIC", "CO"],
            ["CO-APERIODIC", "CO"],
        ],
    }


def goldbach_proof_dag() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "GB-T232", "label": "PrimeWeightedRationalShellAutocorrelationIdentity", "status": "closed"},
            {"id": "GB-SW", "label": "SiegelWalfiszThetaInProgressions", "status": "established_external_theorem"},
            {"id": "GB-T233", "label": "PolylogarithmicSquarefreePrimeShellAsymptoticAndSparseDenominatorNoGo", "status": "closed"},
            {"id": "GB-N233", "label": "UnrestrictedGrowingDenominatorPrimeShellAsymptotic", "status": "refuted_or_limited"},
            {"id": "GB-OPEN233", "label": "UniformTargetAlignedBinaryPrimeMinorArcNegativeMassBelowPolylogMajorArcMargin", "status": "highest_risk_open"},
            {"id": "GB", "label": "StrongGoldbachConjecture", "status": "open_not_proven"},
        ],
        "edges": [
            ["GB-T232", "GB-T233"],
            ["GB-SW", "GB-T233"],
            ["GB-T233", "GB-N233"],
            ["GB-T233", "GB-OPEN233"],
            ["GB-OPEN233", "GB"],
        ],
    }


def make_section(
    problem_id: str,
    ticket_id: str,
    theorem_name: str,
    proposition: str,
    argument: str,
    computation: dict[str, Any],
    logical_limit: str,
    discard: str,
    retain: str,
    next_lemma: str,
    dag: dict[str, Any],
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "theorem_name": theorem_name,
        "declared_proposition": proposition,
        "mathematical_argument": argument,
        "reproducible_computation": computation,
        "logical_limit": logical_limit,
        "route_decision": {
            "discard": discard,
            "retain": retain,
            "next_single_lemma": next_lemma,
        },
        "proof_dag": dag,
    }


def build_audit() -> dict[str, Any]:
    rh_comp = riemann_logarithmic_frame_audit()
    co_comp = collatz_density_band_audit()
    gb_comp = goldbach_shell_audit()
    tp_comp = twin_entropy_audit()

    riemann = make_section(
        "riemann",
        "RH-TICKET-233",
        "LogarithmicAdaptiveScalarFrameExistenceAndSharpDimensionThreshold",
        rh_comp["theorem"],
        rh_comp["proof"],
        rh_comp,
        rh_comp["no_go_scope"],
        "superlogarithmic effective dimension as a necessary scalar-frame condition",
        "transfer the sharp logarithmic scalar frame to the actual signed Weil kernel with an explicit tail budget",
        "LogarithmicAdaptiveScalarFrameToWeilKernelTransferWithExplicitSignedTailDominance",
        generic_proof_dag(
            "RH",
            "LogarithmicAdaptiveScalarFrameExistenceAndSharpDimensionThreshold",
            "SuperlogarithmicScalarEffectiveDimensionNecessity",
            "LogarithmicAdaptiveScalarFrameToWeilKernelTransferWithExplicitSignedTailDominance",
            "RiemannHypothesis",
        ),
    )
    collatz = make_section(
        "collatz",
        "CO-TICKET-233",
        "BinaryLineageCorrectionTwelveOneExclusionAndFixedStratumNoGo",
        co_comp["theorem"],
        co_comp["proof"],
        co_comp,
        co_comp["no_go_scope"],
        "reopening already-closed k<=11 binary layers or iterating a finite fixed-multiplicity ladder as a cofinal proof",
        "attack primitive binary necklaces uniformly across the unbounded admissible density band from k=13 onward",
        "UniformBinaryDensityBandPrimitiveNecklaceNondivisibility",
        collatz_proof_dag(),
    )
    goldbach = make_section(
        "goldbach",
        "GB-TICKET-233",
        "PolylogarithmicSquarefreePrimeShellAsymptoticAndSparseDenominatorNoGo",
        gb_comp["theorem"],
        gb_comp["proof"],
        gb_comp,
        gb_comp["no_go_scope"],
        "uncoupled all-growing-denominator asymptotics, O(1/l) generic classwise inference, and RMS-to-maximum promotion",
        "use the now-controlled polylogarithmic rational centers as the positive major-arc margin and bound target-aligned minor-arc negative mass",
        "UniformTargetAlignedBinaryPrimeMinorArcNegativeMassBelowPolylogMajorArcMargin",
        goldbach_proof_dag(),
    )
    twin = make_section(
        "twin-prime",
        "TP-TICKET-233",
        "CriticalEntropyDampedSignedCRTLargeSieveAndParityRetentionNoGo",
        tp_comp["theorem"],
        tp_comp["proof"],
        tp_comp,
        tp_comp["no_go_scope"],
        "critical product-entropy damping plus centered marginals as a universal signed saving, or bounded product entropy with full-parity retention",
        "prove critical-noise decay for the actual prime-weighted Type-II pushforward before a separate parity-retaining transfer",
        "PrimeWeightedCriticalNoiseCRTChiSquareDecayAtTwinScale",
        generic_proof_dag(
            "TP",
            "CriticalEntropyDampedSignedCRTLargeSieveAndParityRetentionNoGo",
            "CriticalEntropyPlusCenteredMarginalsImpliesSignedSaving",
            "PrimeWeightedCriticalNoiseCRTChiSquareDecayAtTwinScale",
            "TwinPrimeConjecture",
        ),
    )
    tracks = [riemann, collatz, goldbach, twin]
    machine = {
        "exact_partial_theorem_count": 4,
        "refuted_or_corrected_route_count": 4,
        "next_single_lemma_count": 4,
        "proof_dag_count": 4,
        "lineage_regression_correction_count": 1,
        "conjecture_resolution_count": 0,
        "total_failure_count": sum(
            track["reproducible_computation"]["failure_count"] for track in tracks
        ),
    }
    root = {
        "theorem_name": "FourConjectureLogarithmicFrameDensityShellEntropyAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-233 proves a sharp logarithmic scalar-frame construction, "
            "corrects a Collatz proof-DAG regression, closes the first open "
            "binary fixed stratum k=12, and proves a fixed-multiplicity no-go, "
            "proves the polylogarithmic squarefree Goldbach rational-shell "
            "asymptotic with an unrestricted-growth counterfamily, and proves "
            "critical product-entropy CRT bounds and parity-retention no-gos. "
            "It resolves none of the four parent conjectures."
        ),
        "riemann": riemann,
        "collatz": collatz,
        "goldbach": goldbach,
        "twin_prime": twin,
        "machine_audit": machine,
    }
    attempts = []
    for track in tracks:
        attempts.append(
            {
                "ticket_id": track["ticket_id"],
                "problem_id": track["problem_id"],
                "status": STATUS,
                "declared_proposition": track["declared_proposition"],
                "mathematical_argument": track["mathematical_argument"],
                "new_result": track["theorem_name"],
                "discarded_route": track["route_decision"]["discard"],
                "remaining_gap": track["logical_limit"],
                "candidate_theorem": track["route_decision"]["next_single_lemma"],
                "claim_boundary": track["logical_limit"],
                "proof_dag": track["proof_dag"],
                "bounded_result": {
                    "audit_ref": f"#/{AUDIT_KEY}/{track['problem_id'].replace('-', '_')}",
                    "failure_count": track["reproducible_computation"]["failure_count"],
                },
            }
        )
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": (
            "TICKET-233 proves four exact partial, asymptotic, lineage-correction, "
            "or no-go results and resolves none of the four parent conjectures."
        ),
        AUDIT_KEY: root,
        "attempts": attempts,
    }


def write_outputs(audit: dict[str, Any]) -> None:
    root = audit[AUDIT_KEY]
    write_json(
        ROOT / "data/open-problem/ticket233-logarithmic-frame-density-shell-entropy.json",
        audit,
    )
    destinations = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-233-logarithmic-scalar-frame.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-233-density-band-lineage.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-233-polylog-squarefree-shell.json",
        "twin_prime": ROOT / "data/open-problem/twin-prime/tp-ticket-233-critical-entropy-damping.json",
    }
    for key, destination in destinations.items():
        write_json(
            destination,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": STATUS,
                **root[key],
            },
        )


def main() -> None:
    audit = build_audit()
    write_outputs(audit)
    machine = audit[AUDIT_KEY]["machine_audit"]
    print(json.dumps(machine, indent=2))
    if machine["total_failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
