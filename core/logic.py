import itertools
import re

# --- TRUTH TABLES ---
def extract_variables(expr: str) -> list[str]:
    """Finds all distinct uppercase propositional variables (e.g., P, Q, R)."""
    return sorted(list(set(re.findall(r"\b[A-Z]\b", expr))))


def truth_table(expression: str) -> tuple[list[str], list[list[str]]]:
    """
    Generates a truth table for a given boolean expression using variables P, Q, R, etc.
    Returns (headers, rows) compatible with Pandas DataFrames.
    """
    tokens = [ch for ch in expression if ch.isupper() and ch.isalpha()]
    variables = sorted(list(set(tokens)))
    
    if not variables:
        variables = ["P"]

    headers = variables + [expression]
    rows = []

    for combination in itertools.product([True, False], repeat=len(variables)):
        env = dict(zip(variables, combination))
        try:
            result = bool(eval(expression, {"__builtins__": {}}, env))
        except Exception:
            result = False

        row = ["T" if env[v] else "F" for v in variables]
        row.append("T" if result else "F")
        rows.append(row)

    return headers, rows


def generate_truth_table(expression: str):
    """Compatibility alias for CLI."""
    return truth_table(expression)


# --- SET OPERATIONS ---
def set_operations(set_a: set, set_b: set) -> dict:
    """Computes basic set algebra operations."""
    return {
        "Union (A ∪ B)": sorted(list(set_a | set_b)),
        "Intersection (A ∩ B)": sorted(list(set_a & set_b)),
        "Difference (A - B)": sorted(list(set_a - set_b)),
        "Difference (B - A)": sorted(list(set_b - set_a)),
        "Symmetric Difference (A △ B)": sorted(list(set_a ^ set_b)),
        "Cartesian Product (A × B)": [(a, b) for a in sorted(set_a) for b in sorted(set_b)]
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
def classify_relation(domain: set, relation_pairs: set[tuple]) -> dict[str, bool]:
    """
    Classifies a binary relation on a set:
    Reflexive, Symmetric, Transitive, and Equivalence Relation.
    """
    is_reflexive = all((x, x) in relation_pairs for x in domain)
    is_symmetric = all((b, a) in relation_pairs for (a, b) in relation_pairs)

    is_transitive = True
    for (a, b) in relation_pairs:
        for (c, d) in relation_pairs:
            if b == c and (a, d) not in relation_pairs:
                is_transitive = False
                break
        if not is_transitive:
            break

    is_equivalence = is_reflexive and is_symmetric and is_transitive

    return {
        "Reflexive": is_reflexive,
        "Symmetric": is_symmetric,
        "Transitive": is_transitive,
        "Equivalence Relation": is_equivalence
    }


def analyze_relation(domain: set, relation: set[tuple]) -> dict[str, bool]:
    """Alias for backwards compatibility."""
    return classify_relation(domain, relation)
