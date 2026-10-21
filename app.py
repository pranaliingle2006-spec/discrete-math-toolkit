import streamlit as st
import ast
import pandas as pd
from core.logic import truth_table, set_operations, classify_relation
from core.combinatorics import permutations, combinations, derangements, stars_and_bars
from core.number_theory import prime_factors, mod_inverse, crt, extended_gcd
from core.crypto import generate_rsa_keys, rsa_encrypt, rsa_decrypt, affine_encrypt, affine_decrypt
from core.graph_engine import Graph
from core.storage import get_recent_history

# -------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -------------------------------------------------------------
st.set_page_config(
    page_title="Discrete Math Studio",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Soft Lavender Glassmorphism Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Soft Lavender Gradient Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(187, 154, 247, 0.15) 0%, rgba(122, 162, 247, 0.08) 100%);
        border: 1px solid rgba(187, 154, 247, 0.25);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #bb9af7 0%, #c0caf5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        color: #9aa5ce;
        font-size: 1.05rem;
        margin-top: 6px;
    }

    /* Glass Cards for Educational Breakdowns */
    .edu-card {
        background: rgba(26, 27, 38, 0.7);
        border: 1px solid rgba(86, 95, 137, 0.35);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .edu-badge {
        display: inline-block;
        background: rgba(187, 154, 247, 0.18);
        color: #bb9af7;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 10px;
    }

    /* Tab enhancements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 27, 38, 0.4);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(86, 95, 137, 0.25);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        color: #7aa2f7;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(187, 154, 247, 0.2) !important;
        color: #bb9af7 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TOP HERO BANNER
# -------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔮 Discrete Mathematics Learning Studio</div>
    <div class="hero-subtitle">Interactive algorithmic explorations, step-by-step mathematical proofs, and applied cryptosystems.</div>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab_graph, tab_crypto, tab_logic, tab_num, tab_comb, tab_audit = st.tabs([
    "🕸️ Graph Playground",
    "🔐 RSA & Cryptography Lab",
    "⚖️ Truth Tables & Sets",
    "🔢 Modular Arithmetic & CRT",
    "🎲 Combinatorics Engine",
    "📜 Session History"
])

# -------------------------------------------------------------
# 1. GRAPH PLAYGROUND
# -------------------------------------------------------------
with tab_graph:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Graph Theory</span>
        <h4 style="margin: 0; color: #c0caf5;">Interactive Network Analyzer & Physics Visualizer</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Construct custom graph topologies to inspect <b>bipartiteness, connectivity, Euler paths, cycle bounds</b>, and degree-scaled dynamic layouts in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Graph Construction")
        preset = st.selectbox(
            "Load a Standard Topology Preset",
            ["Custom", "Cycle Graph C5", "Complete Graph K5", "Petersen Graph (Preview)", "Star Graph S6"]
        )
        
        preset_edges = {
            "Custom": "[(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]",
            "Cycle Graph C5": "[(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]",
            "Complete Graph K5": "[(1,2), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,4), (3,5), (4,5)]",
            "Petersen Graph (Preview)": "[(1,2), (2,3), (3,4), (4,5), (5,1), (1,6), (2,7), (3,8), (4,9), (5,10), (6,8), (8,10), (10,7), (7,9), (9,6)]",
            "Star Graph S6": "[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]"
        }
        
        edges_input = st.text_area(
            "Edge Tuples",
            value=preset_edges[preset],
            height=120,
            help="Specify edge connections using standard (u, v) pairs."
        )
        is_directed = st.toggle("Directed Network", value=False)
        render_btn = st.button("Analyze & Render Graph", type="primary", use_container_width=True)

    with col_view:
        if render_btn or preset != "Custom":
            try:
                edges = ast.literal_eval(edges_input)
                g = Graph(directed=is_directed)
                for u, v in edges:
                    g.add_edge(str(u), str(v))
                
                # Topological Indicators
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Order |V|", len(g.nodes))
                m2.metric("Size |E|", len(edges))
                m3.metric("Components", len(g.connected_components()))
                has_cycle = g.has_cycle()
                m4.metric("Contains Cycle?", "Yes" if has_cycle else "No", delta="Acyclic" if not has_cycle else "Cyclic", delta_color="inverse")
                
                # Render Pyvis HTML
                html_file = g.visualize_to_html(open_browser=False)
                with open(html_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                st.components.v1.html(html_content, height=620, scrolling=False)
                
                with st.expander("🔬 View Adjacency & Incidence Matrix"):
                    nodes, adj_matrix = g.get_adjacency_matrix()
                    adj_df = pd.DataFrame(adj_matrix, index=nodes, columns=nodes)
                    st.write("**Adjacency Matrix $A(G)$:**")
                    st.dataframe(adj_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error parsing graph structure: {e}")

# -------------------------------------------------------------
# 2. RSA & CRYPTOGRAPHY LAB
# -------------------------------------------------------------
with tab_crypto:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Applied Cryptography</span>
        <h4 style="margin: 0; color: #c0caf5;">Asymmetric & Modular Cryptographic Demonstrator</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            See how the <b>Extended Euclidean Algorithm</b> and <b>Euler's Totient Theorem</b> power modern digital security through verifiable trapdoor functions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    crypto_mode = st.radio("Select Cryptosystem", ["RSA Public-Key Algorithm", "Affine Shift Cipher"], horizontal=True)

    if crypto_mode == "RSA Public-Key Algorithm":
        c_in, c_out = st.columns([1, 1])
        with c_in:
            st.subheader("1. Message Transmission")
            plain_msg = st.text_input("Plaintext Message", value="DISCRETE MATH")
            regen_keys = st.button("Generate Fresh RSA Keypair", type="primary")

        with c_out:
            st.subheader("2. Cryptographic Execution")
            keys = generate_rsa_keys()
            cipher = rsa_encrypt(plain_msg, keys["public_key"])
            decrypted = rsa_decrypt(cipher, keys["private_key"])
            
            st.markdown(f"""
            * **Prime Factors:** $p = {keys['p']}, \\; q = {keys['q']}$
            * **Modulus ($n = p \\times q$):** `{keys['public_key'][1]}`
            * **Euler's Totient $\\phi(n) = (p-1)(q-1)$:** `{keys['phi']}`
            * **Public Key $(e, n)$:** `({keys['public_key'][0]}, {keys['public_key'][1]})`
            * **Private Exponent $d = e^{{-1}} \\pmod{{\\phi(n)}}$:** `{keys['private_key'][0]}`
            """)
            st.code(f"Encrypted Cipher Numbers:\n{cipher}", language="python")
            st.success(f"Verified Decrypted Output: **{decrypted}**")

    else:
        st.subheader("Affine Cipher: $E(x) = (a \\cdot x + b) \\pmod{26}$")
        col_a, col_b, col_t = st.columns(3)
        msg_aff = col_t.text_input("Plaintext / Ciphertext", value="HELLOMATH")
        a_key = col_a.number_input("Multiplier (a coprime with 26)", value=5, min_value=1, max_value=25, step=2)
        b_key = col_b.number_input("Additive Shift (b)", value=8, min_value=0, max_value=25)
        
        gcd_val, _, _ = extended_gcd(int(a_key), 26)
        if gcd_val != 1:
            st.error(f"Cannot use $a = {a_key}$! $\\gcd({a_key}, 26) = {gcd_val} \\neq 1$. Key must be coprime to 26.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                enc = affine_encrypt(msg_aff, int(a_key), int(b_key))
                st.write(f"Encrypted Output: **`{enc}`**")
            with c2:
                dec = affine_decrypt(enc, int(a_key), int(b_key))
                st.write(f"Decrypted Verification: **`{dec}`**")

# -------------------------------------------------------------
# 3. TRUTH TABLES & SETS
# -------------------------------------------------------------
with tab_logic:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Propositional Logic & Set Theory</span>
        <h4 style="margin: 0; color: #c0caf5;">Boolean Evaluation & Equivalence Verification</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Evaluate arbitrary logic propositions ($2^n$ interpretations) and verify binary relations across mathematical domains.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tool = st.selectbox("Select Tool", ["Truth Table Generator", "Binary Relation Classifier", "Set Algebra"])

    if tool == "Truth Table Generator":
        sample_expr = st.selectbox("Load Expression Preset", ["P and (not Q)", "(P or Q) and (not P)", "(P and Q) or (not P and not Q)"])
        expr = st.text_input("Boolean Formula (Uppercase variables, Python operators: and, or, not)", value=sample_expr)
        
        if st.button("Evaluate Truth Table", type="primary"):
            try:
                headers, rows = truth_table(expr)
                df = pd.DataFrame(rows, columns=headers)
                
                # Check for Tautology / Contradiction
                final_col = df[expr]
                if all(val == "T" for val in final_col):
                    st.success("Result: The proposition is a **TAUTOLOGY** (Always True).")
                elif all(val == "F" for val in final_col):
                    st.error("Result: The proposition is a **CONTRADICTION** (Always False).")
                else:
                    st.info("Result: The proposition is **CONTINGENT** (Satisfiable).")
                
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Syntax Error in Boolean Expression: {e}")

    elif tool == "Binary Relation Classifier":
        st.write("Determine if a relation $R \\subseteq A \\times A$ is an **Equivalence Relation**.")
        c1, c2 = st.columns(2)
        dom_in = c1.text_input("Domain Set A (comma-separated)", "1, 2, 3")
        pairs_in = c2.text_input("Relation Pairs R", "[(1,1), (2,2), (3,3), (1,2), (2,1)]")
        
        if st.button("Classify Relation Properties"):
            try:
                dom = set([x.strip() for x in dom_in.split(",") if x.strip()])
                pairs = set(ast.literal_eval(pairs_in))
                str_pairs = {(str(x), str(y)) for x, y in pairs}
                res = classify_relation(dom, str_pairs)
                
                for prop, is_valid in res.items():
                    if is_valid:
                        st.success(f"✔ **{prop}**: Valid")
                    else:
                        st.error(f"✖ **{prop}**: Not Satisfied")
            except Exception as e:
                st.error(f"Input Error: {e}")

    elif tool == "Set Algebra":
        c1, c2 = st.columns(2)
        s_a = c1.text_input("Set A", "1, 2, 3, 4")
        s_b = c2.text_input("Set B", "3, 4, 5, 6")
        
        if st.button("Compute Operations"):
            set_a = set([x.strip() for x in s_a.split(",") if x.strip()])
            set_b = set([x.strip() for x in s_b.split(",") if x.strip()])
            res = set_operations(set_a, set_b)
            st.json(res)

# -------------------------------------------------------------
# 4. NUMBER THEORY & CRT
# -------------------------------------------------------------
with tab_num:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Number Theory</span>
        <h4 style="margin: 0; color: #c0caf5;">Modular Arithmetic & The Chinese Remainder Theorem</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Compute Bézout coefficients, coprime modular inverses, and simultaneous modular congruences.
        </p>
    </div>
    """, unsafe_allow_html=True)

    calc = st.selectbox("Select Technique", ["Extended Euclidean Algorithm & Inverse", "Chinese Remainder Theorem", "Prime Factorization"])

    if calc == "Extended Euclidean Algorithm & Inverse":
        c1, c2 = st.columns(2)
        a_val = c1.number_input("Integer a", value=17, step=1)
        m_val = c2.number_input("Modulus m", value=43, step=1)
        
        if st.button("Calculate Modular Inverse"):
            try:
                g, x, y = extended_gcd(int(a_val), int(m_val))
                inv = mod_inverse(int(a_val), int(m_val))
                proof_mod = (int(a_val) * int(inv)) % int(m_val)
                
                st.markdown(f"""
                ### Step-by-Step Bézout Solution:
                * $\\gcd({a_val}, {m_val}) = {g}$
                * Bézout's Identity: $({a_val})({x}) + ({m_val})({y}) = {g}$
                * Modular Multiplicative Inverse: **$a^{{-1}} \\equiv {inv} \\pmod{{{m_val}}}$**
                *proof_mod = (int(a_val) * int(inv)) % int(m_val)
                st.markdown(f"""
                ### Step-by-Step Bézout Solution:
                * $\\gcd({a_val}, {m_val}) = {g}$
                * Bézout's Identity: $({a_val})({x}) + ({m_val})({y}) = {g}$
                * Modular Multiplicative Inverse: **$a^{{-1}} \\equiv {inv} \\pmod{{{m_val}}}$**
                * Proof: $({a_val} \\times {inv}) \\pmod{{{m_val}}} = {proof_mod}$
                " " ")
            except Exception as e:
                st.error(f"Calculation Error: {e}")

    elif calc == "Chinese Remainder Theorem":

    elif calc == "Chinese Remainder Theorem":
        st.write("Solve systems of congruences: $x \\equiv r_i \\pmod{m_i}$")
        c1, c2 = st.columns(2)
        r_in = c1.text_input("Remainders $r_i$ (comma-separated)", "2, 3, 2")
        m_in = c2.text_input("Moduli $m_i$ (pairwise coprime)", "3, 5, 7")
        
        if st.button("Solve System"):
            try:
                r_vals = [int(x.strip()) for x in r_in.split(",")]
                m_vals = [int(x.strip()) for x in m_in.split(",")]
                ans, total_mod = crt(r_vals, m_vals)
                
                st.success(f"Unique Solution modulo $M = {total_mod}$:")
                st.markdown(f"### $$x \\equiv {ans} \\pmod{{{total_mod}}}$$")
            except Exception as e:
                st.error(f"Error solving CRT: {e}")

    elif calc == "Prime Factorization":
        num = st.number_input("Integer n to factor", value=360, min_value=2)
        if st.button("Factorize"):
            factors = prime_factors(int(num))
            st.write(f"Prime Decomposition of ${num}$: **`{factors}`**")

# -------------------------------------------------------------
# 5. COMBINATORICS ENGINE
# -------------------------------------------------------------
with tab_comb:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Counting & Combinatorics</span>
        <h4 style="margin: 0; color: #c0caf5;">Combinatorial Distributions & Derangements</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Calculate permutations, combinations, partitions (Stars and Bars), and fixed-point-free permutations ($!n$).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    n_param = col1.number_input("Total Elements (n)", min_value=0, max_value=60, value=6, step=1)
    r_param = col2.number_input("Selected Elements / Bins (r)", min_value=0, max_value=60, value=3, step=1)

    p = permutations(int(n_param), int(r_param))
    c = combinations(int(n_param), int(r_param))
    d = derangements(int(n_param))
    sb = stars_and_bars(int(n_param), int(r_param))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"Permutations P({n_param}, {r_param})", f"{p:,}")
    m2.metric(f"Combinations C({n_param}, {r_param})", f"{c:,}")
    m3.metric(f"Derangements !{n_param}", f"{d:,}")
    m4.metric(f"Stars & Bars", f"{sb:,}")

# -------------------------------------------------------------
# 6. SESSION AUDIT LOG
# -------------------------------------------------------------
with tab_audit:
    st.subheader("Offline Session Audit Log (SQLite)")
    st.write("All operations across the CLI and Web App are preserved locally inside `discrete_math_toolkit.db`.")
    logs = get_recent_history(limit=100)
    if logs:
        log_df = pd.DataFrame(logs, columns=["ID", "Module", "Expression / Call", "Output Summary", "Timestamp"])
        st.dataframe(log_df, use_container_width=True)
    else:
        st.info("No calculations logged in this session yet.")
