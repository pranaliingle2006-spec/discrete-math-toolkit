import itertools
import re

# --- TRUTH TABLES ---
def extract_variables(expr: str) -> list[str]:
    """Finds all distinct uppercase propositional variables (e.g., P, Q, R)."""
    return sorted(list(set(re.findall(r"\b[A-Z]\b", expr))))

def generate_truth_table(expression: str):
    """Evaluates a boolean proposition across all True/False assignments."""
    variables = extract_variables(expression)
    rows = []
    for values in itertools.product([True, False], repeat=len(variables)):
        env = dict(zip(variables, values))
        try:
            val = bool(eval(expression, {"__builtins__": {}}, env))
        except Exception as e:
            raise ValueError(f"Invalid boolean expression: {e}")
        rows.append((env, val))
    return variables, rows

# --- SET OPERATIONS ---
def set_operations(set_a: set, set_b: set) -> dict[str, set]:
    """Computes union, intersection, differences, and Cartesian product."""
    return {
        "union": set_a | set_b,
        "intersection": set_a & set_b,
        "difference_A_minus_B": set_a - set_b,
        "difference_B_minus_A": set_b - set_a,
        "symmetric_difference": set_a ^ set_b,
    }

def power_set(s: set) -> list[set]:
    """Generates the power set P(S)."""
    s_list = list(s)
    ps = []
    for r in range(len(s_list) + 1):
        for combo in itertools.combinations(s_list, r):
            ps.append(set(combo))
    return ps

# --- RELATION PROPERTY ANALYZER ---
def analyze_relation(domain: set, relation: set[tuple]) -> dict[str, bool]:
    """
    Checks if a binary relation R on a domain A is:
    - Reflexive: (a, a) in R for all a in A
    - Symmetric: if (a, b) in R then (b, a) in R
    - Transitive: if (a, b) in R and (b, c) in R then (a, c) in R
    - Equivalence: reflexive, symmetric, and transitive
    """
    # Reflexivity
    is_reflexive = all((a, a) in relation for a in domain)

    # Symmetry
    is_symmetric = all((b, a) in relation for (a, b) in relation)

    # Transitivity
    is_transitive = True
    for (a, b) in relation:
        for (c, d) in relation:
            if b == c and (a, d) not in relation:
                is_transitive = False
                break
        if not is_transitive:
            break

    is_equivalence = is_reflexive and is_symmetric and is_transitive

    return {
        "reflexive": is_reflexive,
        "symmetric": is_symmetric,
        "transitive": is_transitive,
        "equivalence": is_equivalence,
    }