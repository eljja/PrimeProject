from __future__ import annotations

from math import gcd, isqrt
from random import Random


SMALL_PRIMES: tuple[int, ...] = (
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)


def parse_int(value: int | str) -> int:
    if isinstance(value, int):
        return value
    text = value.strip().replace("_", "")
    if text.lower().startswith("0x"):
        return int(text, 16)
    return int(text, 10)


def is_probable_prime(n: int, rounds: int = 16, rng: Random | None = None) -> bool:
    if n < 2:
        return False
    small_trial_primes = (2,) + SMALL_PRIMES
    for p in small_trial_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    deterministic_bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    bases: list[int] = [a for a in deterministic_bases if a < n - 2]
    if rng is not None:
        while len(bases) < rounds:
            bases.append(rng.randrange(2, n - 2))

    for a in bases[:rounds]:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def next_probable_prime(candidate: int) -> int:
    n = candidate | 1
    while not is_probable_prime(n):
        n += 2
    return n


def random_prime(bits: int, rng: Random) -> int:
    if bits < 8:
        raise ValueError("bits must be at least 8")
    while True:
        candidate = rng.getrandbits(bits)
        candidate |= 1
        candidate |= 1 << (bits - 1)
        candidate |= 1 << (bits - 2)
        if is_probable_prime(candidate, rng=rng):
            return candidate


def fermat_factor_if_close(n: int, max_steps: int) -> tuple[int, int, int] | None:
    a = isqrt(n)
    if a * a < n:
        a += 1
    for steps in range(max_steps + 1):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            if p > 1 and q > 1 and p * q == n:
                return p, q, steps
        a += 1
    return None


def distance_to_next_square(n: int) -> int:
    root = isqrt(n)
    lower = root * root
    upper = (root + 1) * (root + 1)
    return min(n - lower, upper - n)


def product_tree_shared_factors(values: list[int]) -> dict[int, int]:
    product = 1
    for value in values:
        product *= value

    shared: dict[int, int] = {}
    for index, value in enumerate(values):
        other_product_mod = (product // value) % value
        factor = gcd(value, other_product_mod)
        if 1 < factor < value:
            shared[index] = factor
    return shared

