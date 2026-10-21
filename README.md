def extended\_gcd(a: int, b: int):

&#x20;   """Returns (gcd, x, y) such that a\*x + b\*y = gcd."""

&#x20;   if a == 0:

&#x20;       return b, 0, 1

&#x20;   gcd, x1, y1 = extended\_gcd(b % a, a)

&#x20;   x = y1 - (b // a) \* x1

&#x20;   y = x1

&#x20;   return gcd, x, y



def mod\_inverse(a: int, m: int) -> int:

&#x20;   """Computes modular multiplicative inverse of a under modulo m."""

&#x20;   gcd, x, \_ = extended\_gcd(a, m)

&#x20;   if gcd != 1:

&#x20;       raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) != 1")

&#x20;   return (x % m + m) % m



def prime\_factors(n: int) -> dict\[int, int]:

&#x20;   """Returns the prime factorization of n as a dictionary of {prime: power}."""

&#x20;   if n <= 1:

&#x20;       return {}

&#x20;   factors = {}

&#x20;   d = 2

&#x20;   temp = n

&#x20;   while d \* d <= temp:

&#x20;       while temp % d == 0:

&#x20;           factors\[d] = factors.get(d, 0) + 1

&#x20;           temp //= d

&#x20;       d += 1

&#x20;   if temp > 1:

&#x20;       factors\[temp] = factors.get(temp, 0) + 1

&#x20;   return factors



def chinese\_remainder\_theorem(remainders: list\[int], moduli: list\[int]) -> int:

&#x20;   """

&#x20;   Solves a system of congruences:

&#x20;   x ≡ remainders\[i] (mod moduli\[i])

&#x20;   Assumes moduli are pairwise coprime.

&#x20;   """

&#x20;   total = 0

&#x20;   prod = 1

&#x20;   for m in moduli:

&#x20;       prod \*= m



&#x20;   for r\_i, m\_i in zip(remainders, moduli):

&#x20;       m\_partial = prod // m\_i

&#x20;       inv = mod\_inverse(m\_partial, m\_i)

&#x20;       total += r\_i \* m\_partial \* inv



&#x20;   return total % prod

