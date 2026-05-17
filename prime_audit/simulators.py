from __future__ import annotations

from random import Random

from .models import KeyRecord
from .number_theory import next_probable_prime, random_prime


def generate_synthetic_rsa_dataset(
    *,
    bits: int = 128,
    seed: int = 20260517,
) -> list[KeyRecord]:
    """Create toy RSA public moduli for validation only.

    The default bit size is intentionally far below production security levels so tests
    run quickly and no generated key should be mistaken for a real cryptographic key.
    """
    if bits < 64:
        raise ValueError("synthetic RSA bit size must be at least 64")
    rng = Random(seed)
    prime_bits = bits // 2

    normal_p = random_prime(prime_bits, rng)
    normal_q = random_prime(prime_bits, rng)

    shared_p = random_prime(prime_bits, rng)
    shared_q1 = random_prime(prime_bits, rng)
    shared_q2 = random_prime(prime_bits, rng)

    near_p = random_prime(prime_bits, rng)
    near_q = next_probable_prime(near_p + 200)

    increment_seed_p = rng.getrandbits(prime_bits)
    increment_seed_q = rng.getrandbits(prime_bits)
    increment_p = next_probable_prime((increment_seed_p | (1 << (prime_bits - 1))) | 1)
    increment_q = next_probable_prime((increment_seed_q | (1 << (prime_bits - 1))) | 1)
    while abs(increment_q - increment_p) < 1_000_000:
        increment_seed_q = rng.getrandbits(prime_bits)
        increment_q = next_probable_prime((increment_seed_q | (1 << (prime_bits - 1))) | 1)

    return [
        KeyRecord(
            key_id="normal-rsa-1",
            algorithm="rsa",
            value=normal_p * normal_q,
            public_exponent=65537,
            source="synthetic",
            issuer_or_vendor="simulated-normal",
        ),
        KeyRecord(
            key_id="shared-rsa-1",
            algorithm="rsa",
            value=shared_p * shared_q1,
            public_exponent=65537,
            source="synthetic",
            issuer_or_vendor="simulated-shared-prime",
        ),
        KeyRecord(
            key_id="shared-rsa-2",
            algorithm="rsa",
            value=shared_p * shared_q2,
            public_exponent=65537,
            source="synthetic",
            issuer_or_vendor="simulated-shared-prime",
        ),
        KeyRecord(
            key_id="near-square-rsa",
            algorithm="rsa",
            value=near_p * near_q,
            public_exponent=65537,
            source="synthetic",
            issuer_or_vendor="simulated-near-square",
        ),
        KeyRecord(
            key_id="increment-next-prime-rsa",
            algorithm="rsa",
            value=increment_p * increment_q,
            public_exponent=65537,
            source="synthetic",
            issuer_or_vendor="simulated-increment-next-prime",
        ),
    ]


def add_standard_public_primes(records: list[KeyRecord]) -> list[KeyRecord]:
    return records + [
        KeyRecord(
            key_id="curve25519-field",
            algorithm="ecc",
            value=2**255 - 19,
            source="standard-catalog",
            issuer_or_vendor="RFC 7748",
        ),
        KeyRecord(
            key_id="nist-p256-field",
            algorithm="ecc",
            value=2**256 - 2**224 + 2**192 + 2**96 - 1,
            source="standard-catalog",
            issuer_or_vendor="NIST SP 800-186",
        ),
    ]


def records_to_jsonable(records: list[KeyRecord]) -> dict[str, object]:
    return {
        "records": [
            {
                "key_id": record.key_id,
                "algorithm": record.algorithm,
                "value": hex(record.value),
                "public_exponent": record.public_exponent,
                "source": record.source,
                "created_at": record.created_at,
                "issuer_or_vendor": record.issuer_or_vendor,
                **record.metadata,
            }
            for record in records
        ]
    }
