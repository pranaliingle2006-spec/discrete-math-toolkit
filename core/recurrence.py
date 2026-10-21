import math

def fibonacci_sequence(n_terms: int) -> list[int]:
    """Generates the first n Fibonacci numbers."""
    if n_terms <= 0:
        return []
    if n_terms == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n_terms:
        seq.append(seq[-1] + seq[-2])
    return seq

def catalan_number(n: int) -> int:
    """Computes C(n) = (1 / (n + 1)) * (2n choose n)."""
    if n < 0:
        return 0
    return math.comb(2 * n, n) // (n + 1)

def simulate_recurrence(c1: float, c2: float, a0: float, a1: float, steps: int) -> list[float]:
    """Simulates: a_n = c1 * a_{n-1} + c2 * a_{n-2}."""
    seq = [a0, a1]
    for _ in range(2, steps):
        seq.append(c1 * seq[-1] + c2 * seq[-2])
    return seq

def solve_characteristic_roots(c1: float, c2: float) -> tuple[float | complex, float | complex]:
    """
    Solves the characteristic equation r^2 - c1*r - c2 = 0
    for recurrence: a_n - c1*a_{n-1} - c2*a_{n-2} = 0.
    """
    discriminant = c1**2 + 4 * c2
    if discriminant >= 0:
        r1 = (c1 + math.sqrt(discriminant)) / 2
        r2 = (c1 - math.sqrt(discriminant)) / 2
    else:
        real_part = c1 / 2
        imag_part = math.sqrt(-discriminant) / 2
        r1 = complex(real_part, imag_part)
        r2 = complex(real_part, -imag_part)
    return r1, r2