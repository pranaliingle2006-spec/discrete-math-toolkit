import math

# --- BASIC COUNTING ---
def permutations_count(n: int, r: int) -> int:
    """nPr: Permutations without repetition."""
    if r < 0 or r > n:
        return 0
    return math.perm(n, r)

def combinations_count(n: int, r: int) -> int:
    """nCr: Combinations without repetition."""
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)

def arrangements_with_repetition(n: int, r: int) -> int:
    """n^r: Ordered sequences with repetition allowed."""
    return n ** r

def combinations_with_repetition(n: int, r: int) -> int:
    """Stars and bars: C(n + r - 1, r - 1)."""
    if n < 0 or r <= 0:
        return 0
    return math.comb(n + r - 1, r - 1)

def balls_and_bins(balls: int, bins: int, distinguishable_balls: bool = False, distinguishable_bins: bool = True) -> int:
    """
    Standard distributions:
    - Distinguishable balls into Distinguishable bins: bins^balls
    - Indistinguishable balls into Distinguishable bins: C(bins + balls - 1, balls)
    """
    if distinguishable_balls and distinguishable_bins:
        return bins ** balls
    elif not distinguishable_balls and distinguishable_bins:
        return math.comb(bins + balls - 1, balls)
    else:
        raise NotImplementedError("Only distinguishable-bins distributions supported currently.")

# --- ADVANCED COMBINATORICS ---
def derangements_count(n: int) -> int:
    """Subfactorial !n."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    d0, d1 = 1, 0
    for i in range(2, n + 1):
        d0, d1 = d1, (i - 1) * (d1 + d0)
    return d1

def euler_phi(n: int) -> int:
    """Euler's totient phi(n)."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def pigeonhole_min_capacity(items: int, containers: int) -> int:
    """Returns minimum max-load: ceil(items / containers)."""
    return math.ceil(items / containers)

def inclusion_exclusion_2sets(size_a: int, size_b: int, size_intersection: int) -> int:
    """|A U B| = |A| + |B| - |A ∩ B|"""
    return size_a + size_b - size_intersection

# --- ALIASES MATCHING APP.PY IMPORTS ---
permutations = permutations_count
combinations = combinations_count
derangements = derangements_count
stars_and_bars = combinations_with_repetition
