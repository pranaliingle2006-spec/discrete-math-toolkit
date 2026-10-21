import random
from core.number_theory import extended_gcd, mod_inverse, mod_exp

def is_prime_simple(n: int) -> bool:
    """Basic deterministic primality check for small demonstration keys."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_small_prime(start: int = 50, end: int = 200) -> int:
    """Generates a small random prime within a range."""
    primes = [x for x in range(start, end) if is_prime_simple(x)]
    return random.choice(primes)

def generate_rsa_keys(p: int = None, q: int = None):
    """
    Generates an RSA public and private key pair:
    Public key: (e, n)
    Private key: (d, n)
    """
    if p is None or q is None:
        p = generate_small_prime(60, 150)
        q = generate_small_prime(151, 250)
        while p == q:
            q = generate_small_prime(151, 250)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Standard public exponent candidate
    e = 65537
    if e >= phi or extended_gcd(e, phi)[0] != 1:
        for cand in [3, 5, 17, 257, 65537]:
            if cand < phi and extended_gcd(cand, phi)[0] == 1:
                e = cand
                break

    # Private exponent d is the modular inverse of e mod phi(n)
    d = mod_inverse(e, phi)

    return {"public_key": (e, n), "private_key": (d, n), "p": p, "q": q, "phi": phi}

def rsa_encrypt(message: str, public_key: tuple[int, int]) -> list[int]:
    """Encrypts an ASCII string message using public key (e, n)."""
    e, n = public_key
    return [mod_exp(ord(char), e, n) for char in message]

def rsa_decrypt(cipher_tokens: list[int], private_key: tuple[int, int]) -> str:
    """Decrypts a list of ciphertext numbers back to text using private key (d, n)."""
    d, n = private_key
    chars = [chr(mod_exp(c, d, n)) for c in cipher_tokens]
    return "".join(chars)

# --- BONUS: AFFINE CIPHER (E(x) = (a*x + b) mod 26) ---
def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """Encrypts alphabetic text using modular key (a, b)."""
    if extended_gcd(a, 26)[0] != 1:
        raise ValueError(f"Multiplier 'a' ({a}) must be coprime to 26.")
    
    ciphertext = []
    for ch in plaintext.upper():
        if ch.isalpha():
            x = ord(ch) - ord('A')
            enc = (a * x + b) % 26
            ciphertext.append(chr(enc + ord('A')))
        else:
            ciphertext.append(ch)
    return "".join(ciphertext)

def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """Decrypts alphabetic text using modular inverse of key a."""
    a_inv = mod_inverse(a, 26)
    plaintext = []
    for ch in ciphertext.upper():
        if ch.isalpha():
            y = ord(ch) - ord('A')
            dec = (a_inv * (y - b)) % 26
            plaintext.append(chr(dec + ord('A')))
        else:
            plaintext.append(ch)
    return "".join(plaintext)