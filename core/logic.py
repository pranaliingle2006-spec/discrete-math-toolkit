import itertools
import re

def truth_table(expression: str) -> tuple[list[str], list[list[str]]]:
    """Generates a truth table for a boolean expression using variables like P, Q, R."""
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
    """Compatibility wrapper for CLI."""
    return truth_table(expression)


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


def classify_relation(domain: set, relation_pairs: set[tuple]) -> dict[str, bool]:
    """Classifies a binary relation: reflexive, symmetric, transitive, and equivalence."""
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
    """Compatibility alias."""
    return classify_relation(domain, relation)
