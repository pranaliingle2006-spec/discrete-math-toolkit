import typer
import ast
from rich.console import Console
from rich.table import Table

from core.crypto import (
    generate_rsa_keys, rsa_encrypt, rsa_decrypt,
    affine_encrypt, affine_decrypt
)

from core.storage import init_db, save_record, get_recent_history
from core.number_theory import (
    mod_inverse, prime_factors, chinese_remainder_theorem,
    verify_fermats_little_theorem, mod_exp
)
from core.logic import generate_truth_table, set_operations, power_set, analyze_relation
from core.graph_engine import Graph
from core.combinatorics import (
    permutations_count, combinations_count, arrangements_with_repetition,
    combinations_with_repetition, derangements_count, euler_phi,
    pigeonhole_min_capacity, balls_and_bins
)
from core.recurrence import (
    fibonacci_sequence, catalan_number, simulate_recurrence,
    solve_characteristic_roots
)

app = typer.Typer(help="Discrete Math Toolkit CLI")
num_app = typer.Typer(help="Modular Arithmetic & Number Theory")
logic_app = typer.Typer(help="Logic, Sets & Relations")
graph_app = typer.Typer(help="Graph Theory & Networks")
comb_app = typer.Typer(help="Counting & Combinatorics")
rec_app = typer.Typer(help="Recurrence & Generating Functions")
crypto_app = typer.Typer(help="Applied Discrete Cryptography")
app.add_typer(crypto_app, name="crypto")

app.add_typer(num_app, name="number-theory")
app.add_typer(logic_app, name="logic")
app.add_typer(graph_app, name="graph")
app.add_typer(comb_app, name="combinatorics")
app.add_typer(rec_app, name="recurrence")

console = Console()

@app.callback()
def setup():
    init_db()

# --- MODULE 1: LOGIC, SETS & RELATIONS ---
@logic_app.command("truth-table")
def cli_truth_table(
    expression: str = typer.Option(..., "--expression", help="Logic expression, e.g. 'P and (not Q)'")
):
    try:
        variables, rows = generate_truth_table(expression)
        table = Table(title=f"Truth Table: {expression}")
        for var in variables:
            table.add_column(var, justify="center")
        table.add_column("Result", justify="center", style="bold cyan")
        for env, result in rows:
            table.add_row(*[str(env[v]) for v in variables], str(result))
        console.print(table)
        save_record("logic", expression, f"{len(rows)} evaluations")
    except Exception as err:
        console.print(f"[bold red]Error:[/bold red] {err}")

@logic_app.command("sets")
def cli_sets(
    a: str = typer.Option(..., "-a", help="Set A as comma-separated values, e.g. '1,2,3'"),
    b: str = typer.Option(..., "-b", help="Set B as comma-separated values, e.g. '2,3,4'")
):
    set_a = {x.strip() for x in a.split(",")}
    set_b = {x.strip() for x in b.split(",")}
    ops = set_operations(set_a, set_b)
    table = Table(title="Set Operations")
    table.add_column("Operation", style="cyan")
    table.add_column("Result", style="bold green")
    for op, val in ops.items():
        table.add_row(op, str(val))
    console.print(table)
    save_record("logic", f"A={set_a}, B={set_b}", str(ops))

@logic_app.command("relation")
def cli_relation(
    domain: str = typer.Option(..., "--domain", help="Domain elements, e.g. '1,2,3'"),
    pairs: str = typer.Option(..., "--pairs", help="Tuples as string, e.g. '[(1,1), (2,2), (3,3), (1,2), (2,1)]'")
):
    dom = {x.strip() for x in domain.split(",")}
    rel = set(ast.literal_eval(pairs))
    rel_str = {(str(x), str(y)) for x, y in rel}
    props = analyze_relation(dom, rel_str)
    table = Table(title="Relation Property Analysis")
    table.add_column("Property", style="cyan")
    table.add_column("Satisfied", style="bold green")
    for prop, satisfied in props.items():
        table.add_row(prop.capitalize(), str(satisfied))
    console.print(table)
    save_record("logic", f"dom={dom}, rel={pairs}", str(props))

# --- MODULE 2 & 3: COMBINATORICS ---
@comb_app.command("count")
def cli_combinatorics(
    n: int = typer.Option(..., "-n", help="Total items"),
    r: int = typer.Option(..., "-r", help="Selected items")
):
    nPr = permutations_count(n, r)
    nCr = combinations_count(n, r)
    arr_rep = arrangements_with_repetition(n, r)
    comb_rep = combinations_with_repetition(n, r)
    console.print(f"[bold cyan]P({n}, {r}) without repetition:[/bold cyan] {nPr}")
    console.print(f"[bold cyan]C({n}, {r}) without repetition:[/bold cyan] {nCr}")
    console.print(f"[bold cyan]Arrangements with repetition (n^r):[/bold cyan] {arr_rep}")
    console.print(f"[bold cyan]Combinations with repetition (Stars & Bars):[/bold cyan] {comb_rep}")
    save_record("combinatorics", f"n={n}, r={r}", f"P={nPr}, C={nCr}, RepP={arr_rep}, RepC={comb_rep}")

@comb_app.command("balls-and-bins")
def cli_balls_bins(
    balls: int = typer.Option(..., "--balls", help="Number of balls"),
    bins: int = typer.Option(..., "--bins", help="Number of bins"),
    distinguishable: bool = typer.Option(False, "--distinguishable-balls", help="Are balls distinguishable?")
):
    ways = balls_and_bins(balls, bins, distinguishable_balls=distinguishable)
    mode = "Distinguishable" if distinguishable else "Indistinguishable"
    console.print(f"[bold green]Ways to distribute {balls} {mode} balls into {bins} bins:[/bold green] {ways}")
    save_record("combinatorics", f"balls={balls}, bins={bins}, dist={distinguishable}", str(ways))

@comb_app.command("derangements")
def cli_derangements(n: int = typer.Option(..., "-n", help="Number of items")):
    d = derangements_count(n)
    console.print(f"[bold cyan]!{n} (Derangements):[/bold cyan] {d}")
    save_record("combinatorics", f"!{n}", str(d))

@comb_app.command("phi")
def cli_phi(n: int = typer.Option(..., "-n", help="Number to evaluate")):
    val = euler_phi(n)
    console.print(f"[bold cyan]Euler's Totient phi({n}):[/bold cyan] {val}")
    save_record("combinatorics", f"phi({n})", str(val))

@comb_app.command("pigeonhole")
def cli_pigeonhole(
    items: int = typer.Option(..., "--items", help="Number of items (pigeons)"),
    containers: int = typer.Option(..., "--containers", help="Number of containers (pigeonholes)")
):
    min_cap = pigeonhole_min_capacity(items, containers)
    console.print(f"[bold green]At least one container must contain ≥[/bold green] [bold cyan]{min_cap}[/bold cyan] items.")
    save_record("combinatorics", f"items={items}, containers={containers}", str(min_cap))

# --- MODULE 4: RECURRENCE ---
@rec_app.command("fibonacci")
def cli_fib(terms: int = typer.Option(10, "--terms", "-t", help="Number of terms")):
    seq = fibonacci_sequence(terms)
    console.print(f"[bold green]Fibonacci Sequence ({terms} terms):[/bold green] {seq}")
    save_record("recurrence", f"fibonacci({terms})", str(seq))

@rec_app.command("catalan")
def cli_catalan(n: int = typer.Option(..., "-n", help="Index")):
    cat = catalan_number(n)
    console.print(f"[bold green]Catalan C({n}):[/bold green] {cat}")
    save_record("recurrence", f"catalan({n})", str(cat))

@rec_app.command("roots")
def cli_recurrence_roots(
    c1: float = typer.Option(..., "--c1", help="Coefficient of a_{n-1}"),
    c2: float = typer.Option(..., "--c2", help="Coefficient of a_{n-2}")
):
    r1, r2 = solve_characteristic_roots(c1, c2)
    console.print(f"[bold green]Characteristic Roots for a_n = {c1}*a_(n-1) + {c2}*a_(n-2):[/bold green]")
    console.print(f"r1 = {r1}, r2 = {r2}")
    save_record("recurrence", f"roots(c1={c1}, c2={c2})", f"r1={r1}, r2={r2}")

# --- MODULE 5: NUMBER THEORY ---
@num_app.command("mod-inverse")
def cli_mod_inverse(
    a: int = typer.Option(..., "-a", help="The base integer"),
    m: int = typer.Option(..., "-m", help="The modulo value")
):
    try:
        res = mod_inverse(a, m)
        console.print(f"[bold green]Modular Inverse of {a} mod {m}:[/bold green] {res}")
        save_record("number_theory", f"mod_inverse({a}, {m})", str(res))
    except ValueError as err:
        console.print(f"[bold red]Error:[/bold red] {err}")

@num_app.command("factor")
def cli_factorize(n: int = typer.Option(..., "-n", help="Number to factorize")):
    factors = prime_factors(n)
    if not factors:
        console.print(f"[yellow]{n} has no prime factors.[/yellow]")
        return
    factor_str = " * ".join([f"{p}^{exp}" if exp > 1 else f"{p}" for p, exp in factors.items()])
    console.print(f"[bold green]Prime Factors of {n}:[/bold green] {factor_str}")
    save_record("number_theory", f"factor({n})", factor_str)

@num_app.command("crt")
def cli_crt(
    remainders: str = typer.Option(..., "--rem", help="Comma-separated remainders, e.g. '2,3,2'"),
    moduli: str = typer.Option(..., "--mod", help="Comma-separated moduli, e.g. '3,5,7'")
):
    try:
        rem_list = [int(x.strip()) for x in remainders.split(",")]
        mod_list = [int(x.strip()) for x in moduli.split(",")]
        sol = chinese_remainder_theorem(rem_list, mod_list)
        console.print(f"[bold green]CRT Solution x ≡[/bold green] {sol}")
        save_record("number_theory", f"CRT(r={rem_list}, m={mod_list})", str(sol))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@num_app.command("fermat")
def cli_fermat(
    a: int = typer.Option(..., "-a", help="Base integer"),
    p: int = typer.Option(..., "-p", help="Prime modulus")
):
    valid = verify_fermats_little_theorem(a, p)
    res_val = mod_exp(a, p - 1, p)
    console.print(f"[bold green]a^(p-1) mod p = {a}^{p-1} mod {p} =[/bold green] {res_val}")
    console.print(f"[bold cyan]Satisfies Fermat's Little Theorem (== 1):[/bold cyan] {valid}")
    save_record("number_theory", f"fermat({a}, {p})", str(valid))

# --- MODULE 6: GRAPH ---
from rich.panel import Panel
from rich.columns import Columns

@graph_app.command("analyze")
def cli_graph_analyze(
    edges: str = typer.Option(..., "--edges", help="Edges list as string, e.g. '[(1,2), (2,3), (3,1)]'"),
    visualize: bool = typer.Option(False, "--visualize", "-v", help="Open an interactive web visualization in your browser")
):
    try:
        parsed_edges = ast.literal_eval(edges)
        g = Graph(directed=False)
        for u, v in parsed_edges:
            g.add_edge(str(u), str(v))

        start_node = str(parsed_edges[0][0])
        bfs_traversal = g.bfs(start_node)
        dfs_traversal = g.dfs(start_node)
        has_cycle = g.has_cycle()
        is_tree = g.is_tree()
        components = g.connected_components()
        node_labels, matrix = g.get_adjacency_matrix()

        # Visual Dashboard Cards
        stats_text = (
            f"[bold cyan]Total Vertices:[/bold cyan] {len(g.nodes)}\n"
            f"[bold cyan]Total Edges:[/bold cyan] {len(parsed_edges)}\n"
            f"[bold cyan]Components:[/bold cyan] {len(components)}"
        )
        verdict_text = (
            f"[bold magenta]Contains Cycle:[/bold magenta] {'[bold red]Yes[/bold red]' if has_cycle else '[bold green]No[/bold green]'}\n"
            f"[bold magenta]Is Valid Tree:[/bold magenta] {'[bold green]Yes[/bold green]' if is_tree else '[bold red]No[/bold red]'}\n"
            f"[bold magenta]BFS Walk:[/bold magenta] {' → '.join(bfs_traversal)}"
        )

        p1 = Panel(stats_text, title="[bold white]Network Topology[/bold white]", border_style="blue", expand=True)
        p2 = Panel(verdict_text, title="[bold white]Properties & Walk[/bold white]", border_style="green", expand=True)
        console.print(Columns([p1, p2]))

        # Adjacency Matrix Table
        matrix_table = Table(title="Symmetric Adjacency Matrix", show_header=True, header_style="bold magenta")
        matrix_table.add_column("V", justify="center", style="bold yellow")
        for label in node_labels:
            matrix_table.add_column(label, justify="center")
        for i, row in enumerate(matrix):
            matrix_table.add_row(node_labels[i], *[f"[green]{val}[/green]" if val == 1 else "[dim]0[/dim]" for val in row])
        console.print(matrix_table)

        if visualize:
            html_file = g.visualize_to_html()
            console.print(Panel(
                f"[bold green]✔ Interactive UI active![/bold green]\nLaunched [cyan]{html_file}[/cyan] in your default browser.",
                border_style="yellow"
            ))

        summary = f"Nodes={len(g.nodes)}, Cycle={has_cycle}, Tree={is_tree}"
        save_record("graph", edges, summary)
    except Exception as err:
        console.print(Panel(f"[bold red]Execution Error:[/bold red] {err}", border_style="red"))
# --- OFFLINE HISTORY ---
@app.command("history")
def cli_history(limit: int = typer.Option(10, "--limit", "-l", help="Number of records to show")):
    records = get_recent_history(limit)
    if not records:
        console.print("[yellow]No history records found.[/yellow]")
        return
    table = Table(title=f"Last {len(records)} Calculations")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Module", justify="center", style="cyan")
    table.add_column("Expression / Input", justify="left")
    table.add_column("Result", justify="left", style="bold green")
    table.add_column("Timestamp", justify="center", style="dim")
    for row in records:
        table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
    console.print(table)

# --- APPLIED CRYPTOGRAPHY ---
@crypto_app.command("rsa-demo")
def cli_rsa_demo(
    message: str = typer.Option("HELLO", "--message", "-m", help="Message text to encrypt")
):
    keys = generate_rsa_keys()
    e, n = keys["public_key"]
    d, _ = keys["private_key"]
    
    cipher = rsa_encrypt(message, keys["public_key"])
    recovered = rsa_decrypt(cipher, keys["private_key"])
    
    table = Table(title="RSA Cryptosystem Simulation", show_header=True)
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="bold green")
    table.add_row("Primes (p, q)", f"{keys['p']}, {keys['q']}")
    table.add_row("Modulus (n = p * q)", str(n))
    table.add_row("Totient phi(n)", str(keys["phi"]))
    table.add_row("Public Key (e, n)", f"({e}, {n})")
    table.add_row("Private Key (d, n)", f"({d}, {n})")
    table.add_row("Original Text", message)
    table.add_row("Cipher Tokens", str(cipher))
    table.add_row("Decrypted Text", recovered)
    console.print(table)
    
    save_record("crypto", f"RSA('{message}')", f"Cipher={cipher}")

@crypto_app.command("affine")
def cli_affine(
    text: str = typer.Option(..., "--text", "-t", help="Text to encrypt/decrypt"),
    a: int = typer.Option(5, "-a", help="Coprime multiplier mod 26"),
    b: int = typer.Option(8, "-b", help="Shift value mod 26"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    try:
        if decrypt:
            res = affine_decrypt(text, a, b)
            console.print(f"[bold cyan]Decrypted Text:[/bold cyan] {res}")
        else:
            res = affine_encrypt(text, a, b)
            console.print(f"[bold green]Ciphertext:[/bold green] {res}")
        save_record("crypto", f"affine(a={a}, b={b}, dec={decrypt})", res)
    except Exception as err:
        console.print(f"[bold red]Error:[/bold red] {err}")

if __name__ == "__main__":
    app()