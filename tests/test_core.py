import pytest
from core.logic import generate_truth_table, set_operations, power_set, analyze_relation
from core.combinatorics import (
    permutations_count, combinations_count, arrangements_with_repetition,
    combinations_with_repetition, derangements_count, euler_phi, pigeonhole_min_capacity
)
from core.recurrence import fibonacci_sequence, catalan_number, solve_characteristic_roots
from core.number_theory import (
    extended_gcd, mod_inverse, prime_factors, chinese_remainder_theorem,
    verify_fermats_little_theorem
)
from core.graph_engine import Graph

# --- Module 1: Logic & Proofs ---
def test_logic_and_sets():
    vars, rows = generate_truth_table("P and not Q")
    assert len(rows) == 4
    
    # Set Operations
    res = set_operations({1, 2}, {2, 3})
    assert res["union"] == {1, 2, 3}
    assert res["intersection"] == {2}
    assert len(power_set({1, 2})) == 4

    # Relations
    domain = {1, 2}
    equiv_relation = {(1, 1), (2, 2), (1, 2), (2, 1)}
    assert analyze_relation(domain, equiv_relation)["equivalence"] is True

# --- Module 2 & 3: Counting & Combinatorics ---
def test_counting_and_combinatorics():
    assert permutations_count(5, 2) == 20
    assert combinations_count(5, 2) == 10
    assert arrangements_with_repetition(3, 2) == 9
    assert combinations_with_repetition(3, 2) == 6
    assert derangements_count(4) == 9
    assert euler_phi(10) == 4
    assert pigeonhole_min_capacity(10, 3) == 4

# --- Module 4: Recurrence ---
def test_recurrence():
    assert fibonacci_sequence(6) == [0, 1, 1, 2, 3, 5]
    assert catalan_number(4) == 14
    # r^2 - 5r + 6 = 0 -> roots are 3 and 2
    r1, r2 = solve_characteristic_roots(5, -6)
    assert {r1, r2} == {3.0, 2.0}

# --- Module 5: Number Theory ---
def test_number_theory():
    gcd, x, y = extended_gcd(30, 50)
    assert gcd == 10
    assert mod_inverse(3, 11) == 4
    assert prime_factors(360) == {2: 3, 3: 2, 5: 1}
    assert chinese_remainder_theorem([2, 3, 2], [3, 5, 7]) == 23
    assert verify_fermats_little_theorem(3, 7) is True

# --- Module 6: Graph Theory ---
def test_graph_theory():
    g = Graph(directed=False)
    for u, v in [(1, 2), (2, 3), (3, 1)]:
        g.add_edge(str(u), str(v))
    assert g.has_cycle() is True
    assert g.is_tree() is False
    assert len(g.connected_components()) == 1
    assert len(g.dfs("1")) == 3

from core.crypto import generate_rsa_keys, rsa_encrypt, rsa_decrypt, affine_encrypt, affine_decrypt

# --- Module 7: Cryptography ---
def test_cryptography():
    # RSA Keygen, Encrypt & Decrypt
    keys = generate_rsa_keys(p=61, q=53)
    msg = "HELLO"
    cipher = rsa_encrypt(msg, keys["public_key"])
    plain = rsa_decrypt(cipher, keys["private_key"])
    assert plain == msg

    # Affine Cipher
    affine_cipher = affine_encrypt("HELLO", a=5, b=8)
    affine_plain = affine_decrypt(affine_cipher, a=5, b=8)
    assert affine_plain == "HELLO"