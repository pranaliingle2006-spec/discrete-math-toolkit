def extended_gcd(a: int, b: int):
    """Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """Computes modular multiplicative inverse of a under modulo m."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) != 1")
    return (x % m + m) % m


def prime_factors(n: int) -> dict[int, int]:
    """Returns the prime factorization of n as a dictionary of {prime: power}."""
    if n <= 1:
        return {}
    factors = {}
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors


def crt(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
    """
    Solves a system of congruences:
    x ≡ remainders[i] (mod moduli[i])
    Returns (solution, total_modulus).
    """
    total_mod = 1
    for m in moduli:
        total_mod *= m

    ans = 0
    for r_i, m_i in zip(remainders, moduli):
        m_partial = total_mod // m_i
        inv = mod_inverse(m_partial, m_i)
        ans = (ans + r_i * m_partial * inv) % total_mod

    return ans, total_mod


def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> int:
    """Compatibility alias returning integer solution for CLI."""
    sol, _ = crt(remainders, moduli)
    return sol


def mod_exp(base: int, exp: int, mod: int) -> int:
    """Computes (base^exp) % mod efficiently."""
    return pow(base, exp, mod)


def verify_fermats_little_theorem(a: int, p: int) -> bool:
    """
    Fermat's Little Theorem: If p is prime and gcd(a, p) == 1,
    then a^(p-1) ≡ 1 (mod p).
    """
    if a % p == 0:
        return False
    return mod_exp(a, p - 1, p) == 1
