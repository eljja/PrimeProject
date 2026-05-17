from __future__ import annotations

from .number_theory import is_probable_prime


STANDARD_PRIMES: dict[str, int] = {
    "curve25519-field": 2**255 - 19,
    "curve448-field": 2**448 - 2**224 - 1,
    "nist-p256-field": 2**256 - 2**224 + 2**192 + 2**96 - 1,
    "secp256k1-field": 2**256 - 2**32 - 977,
}


def recognize_standard_prime(value: int) -> str | None:
    for name, prime in STANDARD_PRIMES.items():
        if value == prime:
            return name
    return None


def classify_public_prime(value: int) -> dict[str, object]:
    name = recognize_standard_prime(value)
    q = (value - 1) // 2 if value % 2 == 1 else 0
    return {
        "recognized_parameter": name,
        "is_probable_prime": is_probable_prime(value),
        "is_safe_prime": value % 2 == 1 and is_probable_prime(q),
        "bit_length": value.bit_length(),
    }

