import sys
from pathlib import Path

# Add project root directory to Python module search path
root_dir = Path(__file__).parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
import ast
import math
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

# Custom High-End Modern Lavender Glassmorphism Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(187, 154, 247, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(122, 162, 247, 0.06) 0%, transparent 40%),
                    #0e0f18 !important;
        color: #cdd6f4;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 32, 54, 0.6) 0%, rgba(20, 21, 35, 0.8) 100%);
        border: 1px solid rgba(187, 154, 247, 0.2);
        border-radius: 18px;
        padding: 24px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #c0caf5 0%, #bb9af7 50%, #7aa2f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        color: #9aa5ce;
        font-size: 0.95rem;
        margin-top: 6px;
    }

    /* Cards */
    .edu-card {
        background: rgba(22, 24, 40, 0.65);
        border: 1px solid rgba(187, 154, 247, 0.15);
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 18px;
        backdrop-filter: blur(12px);
    }
    .edu-badge {
        display: inline-block;
        background: rgba(187, 154, 247, 0.15);
        color: #bb9af7;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid rgba(187, 154, 247, 0.25);
        margin-bottom: 8px;
    }

    /* Tabs Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(18, 19, 32, 0.7);
        padding: 6px 10px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        color: #a6adc8;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(187, 154, 247, 0.22) 0%, rgba(122, 162, 247, 0.12) 100%) !important;
        border: 1px solid rgba(187, 154, 247, 0.35) !important;
        color: #c0caf5 !important;
        box-shadow: 0 4px 15px rgba(187, 154, 247, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🔮 Discrete Mathematics Learning Studio</h1>
    <p class="hero-subtitle">Interactive algorithmic explorations, step-by-step mathematical proofs, and applied cryptosystems.</p>
</div>
""", unsafe_allow_html=True)

# Tab Navigation
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
        <h4 style="margin: 0; color: #c0caf5;">Interactive Topology Analyzer & Physics Visualizer</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Construct graph topologies to inspect connectivity, bipartite structures, adjacency matrices, and cycle detection.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 1])

    with col_ctrl:
        st.subheader("Graph Construction")
        preset = st.selectbox(
            "Load a Standard Topology Preset",
            ["Custom", "Bipartite Graph K3,3", "Cycle C5 (Odd Cycle - Non-Bipartite)", "Complete K4", "Petersen Graph", "Star Tree"]
        )

        preset_map = {
            "Custom": "[(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]",
            "Bipartite Graph K3,3": "[(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)]",
            "Cycle C5 (Odd Cycle - Non-Bipartite)": "[(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]",
            "Complete K4": "[(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]",
            "Petersen Graph": "[(1,2), (2,3), (3,4), (4,5), (5,1), (1,6), (2,7), (3,8), (4,9), (5,10), (6,8), (8,10), (10,7), (7,9), (9,6)]",
            "Star Tree": "[(1, 2), (1, 3), (1, 4), (1, 5)]"
        }

        edge_input = st.text_area("Edge Tuples (List of pairs)", value=preset_map[preset], height=80)
        is_directed = st.toggle("Directed Network", value=False)
        render_btn = st.button("Analyze & Render Graph", type="primary")

    with col_view:
        if render_btn or edge_input:
            try:
                edges = ast.literal_eval(edge_input)
                g = Graph(directed=is_directed)
                for u, v in edges:
                    g.add_edge(str(u), str(v))

                nodes_list, adj_mat = g.get_adjacency_matrix()
                comps = g.connected_components()
                has_cyc = g.has_cycle()
                is_tr = g.is_tree()
                is_bip, color_map = g.is_bipartite()

                # Metric Cards HUD
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Vertices |V|", len(g.nodes))
                m2.metric("Edges |E|", len(g.edges))
                m3.metric("Components", len(comps))
                m4.metric("Bipartite?", "Yes ✅" if is_bip else "No ❌")

                # Interactive Pyvis Canvas with Bipartite Color Coding
                try:
                    from pyvis.network import Network
                    net = Network(height="320px", width="100%", bgcolor="#0e0f18", font_color="#c0caf5")
                    
                    for node in g.nodes:
                        # Color nodes by 2-color partition if bipartite
                        if is_bip and node in color_map:
                            node_color = "#7aa2f7" if color_map[node] == 0 else "#f7768e"
                        else:
                            node_color = "#bb9af7"
                        net.add_node(node, label=f"V: {node}", color=node_color, size=18)

                    for u, v in g.edges:
                        net.add_edge(u, v, color="#565f89")
                    
                    html_path = "temp_graph.html"
                    net.save_graph(html_path)
                    with open(html_path, "r", encoding="utf-8") as f:
                        st.components.v1.html(f.read(), height=340)
                except Exception as pyvis_err:
                    st.info(f"Pyvis render preview: {pyvis_err}")

            except Exception as e:
                st.error(f"Error parsing graph structure: {e}")

    # ---------------------------------------------------------
    # PEDAGOGICAL BREAKDOWNS & THEORETICAL VERIFICATIONS
    # ---------------------------------------------------------
    if 'g' in locals() and g.nodes:
        st.markdown("---")
        st.subheader("🔬 Deep Graph Analysis & Theoretical Proofs")
        
        c_left, c_right = st.columns(2)

        with c_left:
            with st.expander("🧩 1. Connectivity & Component Decomposition", expanded=True):
                is_connected = len(comps) == 1
                st.markdown(f"""
                * **Status:** {'**Connected Graph** (1 component)' if is_connected else f'**Disconnected Graph** ({len(comps)} components)'}
                * **Formal Definition:** A graph is connected if there is a path between every pair of vertices.
                * **Component Partition ($V = \\bigcup C_i$):**
                """)
                for idx, comp in enumerate(comps):
                    st.markdown(f"  * **Component {idx+1}:** `{{{', '.join(comp)}}}` (Size: {len(comp)})")

            with st.expander("🎨 2. Bipartite Structure & 2-Colorability", expanded=True):
                if is_bip:
                    set_1 = [node for node, c in color_map.items() if c == 0]
                    set_2 = [node for node, c in color_map.items() if c == 1]
                    st.success("✅ **Graph is Bipartite (2-Colorable)**")
                    st.markdown(f"""
                    * **Theorem (Kőnig):** A graph is bipartite if and only if it contains **no odd-length cycles**.
                    * **Independent Set $V_1$ (Blue):** `{{{', '.join(set_1)}}}`
                    * **Independent Set $V_2$ (Red):** `{{{', '.join(set_2)}}}`
                    * **Property:** Every edge in $E$ joins a vertex in $V_1$ to a vertex in $V_2$. No two vertices within the same set share an edge.
                    """)
                else:
                    st.error("❌ **Graph is NOT Bipartite**")
                    st.markdown("""
                    * **Reason:** The graph contains at least one **odd-length cycle** (e.g., a triangle $C_3$ or pentagon $C_5$).
                    * **Consequence:** It is impossible to color the vertices with 2 colors without two adjacent vertices sharing the same color.
                    """)

        with c_right:
            with st.expander("🔄 3. Cycle Detection & Tree Verification", expanded=True):
                st.markdown(f"""
                * **Contains Cycle:** `{'Yes (DFS detected a back-edge)' if has_cyc else 'No (Acyclic / Forest)'}`
                * **Is a Tree:** `{'Yes ✅' if is_tr else 'No ❌'}`
                * **Tree Conditions Verification:**
                  1. **Connectivity Check:** {'✅ Satisfied (1 component)' if len(comps) == 1 else '❌ Failed (Disconnected)'}
                  2. **Acyclic Check:** {'✅ Satisfied (No cycles)' if not has_cyc else '❌ Failed (Contains cycles)'}
                  3. **Euler Characteristic ($|E| = |V| - 1$):**
                     * $|V| = {len(g.nodes)}$
                     * $|E| = {len(g.edges)}$
                     * $|E| = |V| - 1 \implies {len(g.edges)} = {len(g.nodes) - 1}$ {'✅ Holds' if len(g.edges) == len(g.nodes) - 1 else '❌ Does not hold'}
                """)

            with st.expander("📊 4. Adjacency Matrix $A(G)$", expanded=True):
                st.markdown("The matrix entry $A_{i,j} = 1$ if vertex $v_i$ is adjacent to $v_j$, and $0$ otherwise:")
                df_mat = pd.DataFrame(adj_mat, index=nodes_list, columns=nodes_list)
                st.dataframe(df_mat, use_container_width=True)

# -------------------------------------------------------------
# 2. RSA & CRYPTOGRAPHY LAB
# -------------------------------------------------------------
with tab_crypto:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Applied Cryptography</span>
        <h4 style="margin: 0; color: #c0caf5;">Asymmetric RSA & Modular Affine Ciphers</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            See how the <b>Extended Euclidean Algorithm</b> and <b>Euler's Totient Theorem</b> power modern digital security through verifiable trapdoor functions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    crypto_mode = st.radio("Select Cryptosystem", ["RSA Public-Key Cryptosystem", "Affine Substitution Cipher"], horizontal=True)

    if crypto_mode == "RSA Public-Key Cryptosystem":
        if "rsa_keys" not in st.session_state:
            st.session_state.rsa_keys = generate_rsa_keys()

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("1. Keypair Architecture & Parameters")
            if st.button("Generate Fresh Prime Keypair", type="primary"):
                st.session_state.rsa_keys = generate_rsa_keys()
                st.success("New RSA keypair generated successfully!")

            keys = st.session_state.rsa_keys
            p, q = keys["p"], keys["q"]
            e, n = keys["public_key"]
            d, _ = keys["private_key"]
            phi = keys["phi"]

            st.markdown(f"""
            * **Secret Prime $p$:** `{p}`
            * **Secret Prime $q$:** `{q}`
            * **Public Modulus ($n = p \\times q$):** `{n}`
            * **Euler's Totient $\\phi(n) = (p-1)(q-1)$:** `{phi}`
            * **Public Exponent ($e$ coprime to $\\phi(n)$):** `{e}`
            * **Private Exponent ($d = e^{{-1}} \\pmod{{\\phi(n)}}$):** `{d}`
            """)

            with st.expander("🔑 How Key Generation Works (Euler's Totient & Bézout)", expanded=False):
                ed_mod = (e * d) % phi
                st.markdown(f"""
                1. **Choose two primes:** $p = {p}, \\; q = {q}$
                2. **Compute Modulus:** $n = {p} \\times {q} = {n}$ (Publicly shared). Factoring $n$ back into $p, q$ is computationally intractable for large numbers.
                3. **Compute Totient:** $\\phi(n) = ({p}-1)({q}-1) = {phi}$
                4. **Select Public Exponent $e$:** Chosen such that $\\gcd(e, \\phi(n)) = \\gcd({e}, {phi}) = 1$.
                5. **Compute Private Exponent $d$ via Bézout's Identity:**
                   $$e \\cdot d \\equiv 1 \\pmod{{\\phi(n)}}$$
                   $$({e})({d}) \\pmod{{{phi}}} = {ed_mod}$$
                   Anyone knowing $d$ can invert exponentiation modulo $n$.
                """)

        with col_right:
            st.subheader("2. Message Transmission & Proof")
            plain_msg = st.text_input("Plaintext Message to Encrypt", value="HELLO")
            
            if plain_msg:
                cipher_tokens = rsa_encrypt(plain_msg, (e, n))
                decrypted_msg = rsa_decrypt(cipher_tokens, (d, n))

                st.markdown("**Encrypted Cipher Tokens:**")
                st.code(f"{cipher_tokens}", language="python")
                st.success(f"**Verified Decrypted Output:** `{decrypted_msg}`")

        if plain_msg:
            st.markdown("---")
            with st.expander("🔬 Step-by-Step Encryption & Decryption Breakdown", expanded=True):
                st.write("RSA encrypts and decrypts each character by transforming it between letters, ASCII numbers, and modular cipher tokens.")
                
                char_steps = []
                for ch, c_val in zip(plain_msg, cipher_tokens):
                    m_ord = ord(ch)
                    recovered_ord = pow(c_val, d, n)
                    recovered_ch = chr(recovered_ord)
                    char_steps.append({
                        "Plain Character": f"'{ch}'",
                        "ASCII Value (M)": m_ord,
                        "Public Exponent (e)": e,
                        "Modulus (n)": n,
                        "Encrypted Token (C)": c_val,
                        "Private Key (d)": d,
                        "Decrypted ASCII": recovered_ord,
                        "Recovered Character": f"'{recovered_ch}'"
                    })
                
                st.dataframe(pd.DataFrame(char_steps), use_container_width=True)

                first_ch = plain_msg[0]
                first_m = ord(first_ch)
                first_c = cipher_tokens[0]
                first_rec = pow(first_c, d, n)

                st.markdown(f"""
                ### 📖 Example Walkthrough: Encrypting & Decrypting the letter `'{first_ch}'`
                
                1. **Step 1: Convert Letter to Number (ASCII):**
                   * The computer represents `'{first_ch}'` as integer **$M = {first_m}$**.
                
                2. **Step 2: Lock / Encrypt with Public Key $(e = {e}, n = {n})$:**
                   * Formula: $C = M^e \\pmod n$
                   * Math: ${first_m}^{{{e}}} \\pmod{{{n}}} = \\mathbf{{{first_c}}}$
                   * The number **`{first_c}`** is the secret cipher token sent across the wire.
                
                3. **Step 3: Unlock / Decrypt with Private Key $(d = {d}, n = {n})$:**
                   * Formula: $M = C^d \\pmod n$
                   * Math: ${first_c}^{{{d}}} \\pmod{{{n}}} = \\mathbf{{{first_rec}}}$
                
                4. **Step 4: Convert Number Back to Character:**
                   * The integer **${first_rec}$** is converted back to ASCII: **`'{chr(first_rec)}'`** ✅
                """)

    else:
        st.subheader("Affine Cipher: $E(x) = (a \\cdot x + b) \\pmod{26}$")
        col_a, col_b, col_t = st.columns(3)
        msg_aff = col_t.text_input("Plaintext (A-Z)", value="DISCRETE")
        a_key = col_a.number_input("Multiplier a (coprime to 26)", value=5, min_value=1, max_value=25, step=1)
        b_key = col_b.number_input("Additive Shift b", value=8, min_value=0, max_value=25, step=1)

        gcd_val = math.gcd(int(a_key), 26)

        if gcd_val != 1:
            st.error(f"❌ Key $a = {a_key}$ is invalid! $\\gcd({a_key}, 26) = {gcd_val} \\neq 1$. Key must be coprime to 26.")
        else:
            a_inv = mod_inverse(int(a_key), 26)
            enc_text = affine_encrypt(msg_aff, int(a_key), int(b_key))
            dec_text = affine_decrypt(enc_text, int(a_key), int(b_key))

            c_enc, c_dec = st.columns(2)
            c_enc.metric("Encrypted Ciphertext", enc_text)
            c_dec.metric("Decrypted Verification", dec_text)

            with st.expander("📝 Step-by-Step Substitution Walkthrough", expanded=True):
                inv_check = (int(a_key) * a_inv) % 26
                st.markdown(f"""
                #### Key Mathematical Inversion
                * **Encryption Key:** $a = {a_key}, \\; b = {b_key}$
                * **Decryption Key $a^{{-1}} \\pmod{{26}}$:** $({a_key} \\times {a_inv}) \\pmod{{26}} = {inv_check} \\implies \\mathbf{{a^{{-1}} = {a_inv}}}$
                * **Decryption Formula:** 
                  $$D(y) = a^{{-1}}(y - b) \\pmod{{26}} = {a_inv}(y - {b_key}) \\pmod{{26}}$$
                """)

                step_data = []
                for orig_ch, enc_ch in zip(msg_aff.upper(), enc_text):
                    if orig_ch.isalpha():
                        x = ord(orig_ch) - ord('A')
                        y = (int(a_key) * x + int(b_key)) % 26
                        recovered_x = (a_inv * (y - int(b_key))) % 26
                        step_data.append({
                            "Plain Letter": orig_ch,
                            "Index x": x,
                            "Encrypt: (a*x + b) mod 26": f"({a_key} * {x} + {b_key}) mod 26 = {y}",
                            "Cipher Letter": enc_ch,
                            "Decrypt: a^-1(y - b) mod 26": f"{a_inv}({y} - {b_key}) mod 26 = {recovered_x}",
                            "Recovered Letter": chr(recovered_x + ord('A'))
                        })

                if step_data:
                    st.table(pd.DataFrame(step_data))

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

        if st.button("Classify Relation Properties", type="primary"):
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

        if st.button("Compute Operations", type="primary"):
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
            Interactive proofs for Bézout's Identity, modular inverses, simultaneous linear congruences, and prime decompositions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    calc = st.selectbox("Select Technique", [
        "Extended Euclidean Algorithm & Inverse", 
        "Chinese Remainder Theorem", 
        "Prime Factorization & Divisor Analysis"
    ])

    if calc == "Extended Euclidean Algorithm & Inverse":
        st.write("Find $\\gcd(a, m)$, compute Bézout coefficients $x, y$ such that $a \\cdot x + m \\cdot y = \\gcd(a, m)$, and determine the modular multiplicative inverse $a^{-1} \\pmod m$.")
        c1, c2 = st.columns(2)
        a_val = c1.number_input("Integer a", value=17, step=1)
        m_val = c2.number_input("Modulus m", value=43, step=1, min_value=2)

        if st.button("Compute Step-by-Step Solution", type="primary"):
            try:
                a_int = int(a_val)
                m_int = int(m_val)

                steps = []
                temp_a, temp_b = a_int, m_int
                while temp_b != 0:
                    q = temp_a // temp_b
                    r = temp_a % temp_b
                    steps.append({"Dividend": temp_a, "Divisor": temp_b, "Quotient": q, "Remainder": r})
                    temp_a, temp_b = temp_b, r

                g, x, y = extended_gcd(a_int, m_int)

                if g == 1:
                    inv = mod_inverse(a_int, m_int)
                    st.success(f"### Unique Modular Inverse: $a^{{-1}} \\equiv {inv} \\pmod{{{m_int}}}$")
                else:
                    inv = None
                    st.error(f"### Modular Inverse Does Not Exist ($\\gcd({a_int}, {m_int}) = {g} \\neq 1$)")

                with st.expander("📝 Step-by-Step Proof & Division Table", expanded=True):
                    st.markdown("#### Phase 1: Forward Euclidean Division Steps")
                    st.table(pd.DataFrame(steps))

                    st.markdown(f"""
                    #### Phase 2: Bézout's Identity Formulation
                    By reversing the Euclidean steps, integers $x$ and $y$ can be expressed such that:
                    $$({a_int})({x}) + ({m_int})({y}) = \\gcd({a_int}, {m_int}) = {g}$$
                    * **Bézout coefficient for $a$ ($x$):** `{x}`
                    * **Bézout coefficient for $m$ ($y$):** `{y}`
                    """)

                    if g == 1:
                        proof_val = (a_int * inv) % m_int
                        status_label = "✅ Correct (Identity holds)" if proof_val == 1 else "❌ Error"
                        st.markdown(f"""
                        #### Phase 3: Modular Inverse Derivation
                        Modulo ${m_int}$, the term $({m_int})({y}) \\equiv 0 \\pmod{{{m_int}}}$. Therefore:
                        $$({a_int})({x}) \\equiv 1 \\pmod{{{m_int}}}$$
                        Because $x = {x}$ may be negative, we compute the canonical representative:
                        $$x \\pmod{{{m_int}}} = {x} \\pmod{{{m_int}}} = \\mathbf{{{inv}}}$$

                        #### Phase 4: Verification Check
                        $$({a_int} \\times {inv}) = {a_int * inv}$$
                        $$({a_int * inv}) \\pmod{{{m_int}}} = \\mathbf{{{proof_val}}} \\quad \\text{{{status_label}}}$$
                        """)
                    else:
                        st.info(f"Since $\\gcd({a_int}, {m_int}) = {g} > 1$, $a$ and $m$ share a common factor. No integer $x$ can satisfy $a \\cdot x \\equiv 1 \\pmod m$.")

            except Exception as e:
                st.error(f"Calculation Error: {e}")

    elif calc == "Chinese Remainder Theorem":
        st.write("Solve simultaneous modular systems: $x \\equiv r_i \\pmod{m_i}$ where all moduli $m_i$ are pairwise coprime.")
        c1, c2 = st.columns(2)
        r_in = c1.text_input("Remainders $r_i$ (comma-separated)", "2, 3, 2")
        m_in = c2.text_input("Moduli $m_i$ (pairwise coprime)", "3, 5, 7")

        if st.button("Solve System Step-by-Step", type="primary"):
            try:
                r_vals = [int(x.strip()) for x in r_in.split(",") if x.strip()]
                m_vals = [int(x.strip()) for x in m_in.split(",") if x.strip()]

                if len(r_vals) != len(m_vals):
                    st.error("The count of remainders must equal the count of moduli.")
                elif len(r_vals) == 0:
                    st.error("Please enter at least one congruence.")
                else:
                    k = len(m_vals)
                    not_coprime = []
                    for i in range(k):
                        for j in range(i + 1, k):
                            if math.gcd(m_vals[i], m_vals[j]) != 1:
                                not_coprime.append(f"gcd({m_vals[i]}, {m_vals[j]}) = {math.gcd(m_vals[i], m_vals[j])}")

                    if not_coprime:
                        st.error(f"The moduli are not pairwise coprime! Conflicts: {', '.join(not_coprime)}")
                    else:
                        total_M = 1
                        for m in m_vals:
                            total_M *= m

                        table_rows = []
                        terms = []
                        total_sum = 0

                        for i in range(k):
                            r_i = r_vals[i]
                            m_i = m_vals[i]
                            M_i = total_M // m_i
                            y_i = mod_inverse(M_i, m_i)
                            term = r_i * M_i * y_i
                            total_sum += term
                            terms.append(f"({r_i} \\times {M_i} \\times {y_i})")

                            table_rows.append({
                                "Index $i$": i + 1,
                                "Remainder $r_i$": r_i,
                                "Modulus $m_i$": m_i,
                                "Partial Modulus $M_i = M / m_i$": M_i,
                                "Inverse $y_i \\equiv M_i^{-1} \\pmod{m_i}$": y_i,
                                "Product $r_i M_i y_i$": term
                            })

                        ans = total_sum % total_M

                        st.success(f"### Unique Solution: $x \\equiv {ans} \\pmod{{{total_M}}}$")

                        with st.expander("📝 Step-by-Step Constructive Proof", expanded=True):
                            st.markdown(f"""
                            #### Step 1: Compute Total Modulus $M$
                            $$M = \\prod_{{i=1}}^{{{k}}} m_i = {' \\times '.join(str(m) for m in m_vals)} = \\mathbf{{{total_M}}}$$

                            #### Step 2: Compute Partial Moduli & Bézout Inverses
                            For each congruence, compute $M_i = \\frac{{M}}{{m_i}}$ and solve $M_i \\cdot y_i \\equiv 1 \\pmod{{m_i}}$:
                            """)

                            st.table(pd.DataFrame(table_rows))

                            st.markdown(f"""
                            #### Step 3: Formulate the Linear Combination
                            Construct the solution sum:
                            $$x_0 = \\sum_{{i=1}}^{{{k}}} r_i M_i y_i = {' + '.join(terms)}$$
                            $$x_0 = \\mathbf{{{total_sum}}}$$

                            #### Step 4: Canonical Reduction Modulo $M$
                            $$x = x_0 \\pmod{{M}} = {total_sum} \\pmod{{{total_M}}} = \\mathbf{{{ans}}}$$
                            """)

                            st.markdown("#### Step 5: Verification Checklist")
                            verifications = []
                            for i in range(k):
                                actual = ans % m_vals[i]
                                is_ok = (actual == r_vals[i])
                                verifications.append(f"* **Equation {i+1}:** ${ans} \\pmod{{{m_vals[i]}}} = {actual}$ (Target: ${r_vals[i]}$) {'✅ Satisfied' if is_ok else '❌ Failed'}")
                            st.markdown("\n".join(verifications))

            except Exception as e:
                st.error(f"Error solving system: {e}")

    elif calc == "Prime Factorization & Divisor Analysis":
        st.write("Decompose an integer into its unique prime factor representation according to the **Fundamental Theorem of Arithmetic**.")
        num_in = st.number_input("Integer n to factorize", value=360, min_value=2, step=1)

        if st.button("Factorize & Analyze", type="primary"):
            n = int(num_in)
            factors = prime_factors(n)

            decomp_latex = " \\times ".join([f"{p}^{{{exp}}}" if exp > 1 else f"{p}" for p, exp in sorted(factors.items())])
            st.markdown(f"### $${n} = {decomp_latex}$$")

            with st.expander("🔬 Structural Divisor & Totient Breakdown", expanded=True):
                num_divisors = 1
                for exp in factors.values():
                    num_divisors *= (exp + 1)

                phi_val = n
                for p in factors.keys():
                    phi_val = (phi_val * (p - 1)) // p

                c1, c2, c3 = st.columns(3)
                c1.metric("Distinct Prime Bases", len(factors))
                c2.metric("Total Divisors d(n)", num_divisors)
                c3.metric("Euler's Totient φ(n)", phi_val)

                div_formula = " \\times ".join([f"({exp} + 1)" for exp in factors.values()])

                st.markdown(f"""
                * **Fundamental Theorem of Arithmetic:** Every integer $n > 1$ can be represented uniquely as a product of prime powers:
                  $$n = \\prod_{{i=1}}^{{k}} p_i^{{a_i}} = {decomp_latex}$$
                * **Divisor Count Formula $d(n)$:**
                  $$d({n}) = \\prod (a_i + 1) = {div_formula} = \\mathbf{{{num_divisors}}}$$
                * **Euler's Totient $\\phi(n)$ (Coprime Count):**
                  The count of integers in $[1, {n}]$ coprime to ${n}$ is:
                  $$\\phi({n}) = \\mathbf{{{phi_val}}}$$
                """)

# -------------------------------------------------------------
# 5. COMBINATORICS ENGINE
# -------------------------------------------------------------
with tab_comb:
    st.markdown("""
    <div class="edu-card">
        <span class="edu-badge">Module: Counting & Combinatorics</span>
        <h4 style="margin: 0; color: #c0caf5;">Combinatorial Distributions & Derangements</h4>
        <p style="color: #9aa5ce; font-size: 0.95rem; margin-top: 6px;">
            Explore the algebraic foundations of counting: arrangements where order matters, unordered selections, fixed-point-free permutations, and partitioning identical items.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    n_param = col1.number_input("Total Elements (n)", min_value=0, max_value=30, value=5, step=1)
    r_param = col2.number_input("Selected Elements / Bins (r)", min_value=0, max_value=30, value=4, step=1)

    n = int(n_param)
    r = int(r_param)

    p = permutations(n, r)
    c = combinations(n, r)
    d = derangements(n)
    sb = stars_and_bars(n, r)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(f"Permutations P({n}, {r})", f"{p:,}")
    m2.metric(f"Combinations C({n}, {r})", f"{c:,}")
    m3.metric(f"Derangements !{n}", f"{d:,}")
    m4.metric(f"Stars & Bars", f"{sb:,}")

    st.markdown("---")
    st.subheader("📚 Concept Explanations & Step-by-Step Proofs")

    col_left, col_right = st.columns(2)

    with col_left:
        with st.expander("🔹 **Permutations** $P(n, r)$: Order Matters", expanded=True):
            st.markdown(f"""
            * **Concept:** The number of ordered arrangements of $r$ distinct items chosen from a pool of $n$.
            * **Formula:** 
              $$P(n, r) = \\frac{{n!}}{{(n - r)!}}$$
            * **Calculation for $n = {n}, r = {r}$:**
              $$P({n}, {r}) = \\frac{{{n}!}}{{({n} - {r})!}} = \\frac{{{math.factorial(n)}}}{{{math.factorial(max(0, n - r))}}} = \\mathbf{{{p:,}}}$$
            * **Intuition:** Assigning distinct positions or rank (e.g., 1st, 2nd, 3rd place podium finishes among {n} competitors).
            """)

        with st.expander("🔹 **Derangements** $!n$: Zero Fixed Points", expanded=True):
            st.markdown(f"""
            * **Concept:** Permutations of $n$ items such that **no item appears in its original position**.
            * **Recursive Formula:** 
              $$!n = (n - 1)(!(n - 1) + !(n - 2)) \\quad \\text{{with }} !0 = 1, !1 = 0$$
            * **Summation Formula:**
              $$!{n} = {n}! \\sum_{{k=0}}^{{{n}}} \\frac{{(-1)^k}}{{k!}} = \\mathbf{{{d:,}}}$$
            * **Intuition:** The "Secret Santa" problem: {n} people put their names in a hat and draw one out; $!{n}$ is the number of ways nobody draws their own name.
            """)

    with col_right:
        with st.expander("🔹 **Combinations** $C(n, r)$: Order Does Not Matter", expanded=True):
            st.markdown(f"""
            * **Concept:** The number of unordered subsets of $r$ items selected from a collection of $n$.
            * **Formula:** 
              $$C(n, r) = \\binom{{n}}{{r}} = \\frac{{n!}}{{r!(n - r)!}}$$
            * **Calculation for $n = {n}, r = {r}$:**
              $$C({n}, {r}) = \\frac{{{n}!}}{{{r}! \\cdot ({n} - {r})!}} = \\frac{{{math.factorial(n)}}}{{{math.factorial(r)} \\times {math.factorial(max(0, n - r))}}} = \\mathbf{{{c:,}}}$$
            * **Intuition:** Choosing a team or committee of {r} members from a group of {n} candidates (the order they are picked does not create a new team).
            """)

        with st.expander("🔹 **Stars & Bars**: Partitions into Bins", expanded=True):
            st.markdown(f"""
            * **Concept:** Distributing $n$ **indistinguishable** items into $r$ **distinguishable** bins (or finding non-negative integer solutions to $x_1 + x_2 + \\dots + x_r = n$).
            * **Formula:** 
              $$\\binom{{n + r - 1}}{{r - 1}}$$
            * **Calculation for $n = {n}, r = {r}$:**
              $$\\binom{{{n} + {r} - 1}}{{{r} - 1}} = \\binom{{{n + r - 1}}}{{{r - 1}}} = \\mathbf{{{sb:,}}}$$
            * **Intuition:** Placing {r - 1} dividers ("bars") between {n} identical tokens ("stars") to divide them among {r} recipients.
            """)

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
