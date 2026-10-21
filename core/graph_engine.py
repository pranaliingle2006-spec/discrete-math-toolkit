from collections import defaultdict, deque
import webbrowser
import os

class Graph:
    def __init__(self, directed: bool = False):
        self.adj = defaultdict(list)
        self.nodes = set()
        self.edges = []
        self.directed = directed

    def add_edge(self, u: str, v: str):
        self.nodes.add(u)
        self.nodes.add(v)
        self.edges.append((u, v))
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start: str) -> list[str]:
        if start not in self.nodes:
            return []
        visited = set([start])
        queue = deque([start])
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: str) -> list[str]:
        if start not in self.nodes:
            return []
        visited = set()
        order = []

        def _dfs_util(node):
            visited.add(node)
            order.append(node)
            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    _dfs_util(neighbor)

        _dfs_util(start)
        return order

    def connected_components(self) -> list[list[str]]:
        visited = set()
        components = []
        for node in sorted(self.nodes):
            if node not in visited:
                comp = self.bfs(node)
                visited.update(comp)
                components.append(comp)
        return components

    def get_adjacency_matrix(self) -> tuple[list[str], list[list[int]]]:
        node_list = sorted(list(self.nodes))
        node_index = {node: i for i, node in enumerate(node_list)}
        n = len(node_list)
        matrix = [[0] * n for _ in range(n)]
        for u in self.adj:
            for v in self.adj[u]:
                matrix[node_index[u]][node_index[v]] = 1
        return node_list, matrix

    def get_incidence_matrix(self) -> tuple[list[str], list[str], list[list[int]]]:
        node_list = sorted(list(self.nodes))
        node_index = {node: i for i, node in enumerate(node_list)}
        edge_labels = [f"({u},{v})" for u, v in self.edges]
        matrix = [[0] * len(self.edges) for _ in range(len(node_list))]

        for j, (u, v) in enumerate(self.edges):
            matrix[node_index[u]][j] = 1
            matrix[node_index[v]][j] = 1

        return node_list, edge_labels, matrix

    def has_cycle(self) -> bool:
        visited = set()

        def _dfs_cycle(node, parent):
            visited.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if _dfs_cycle(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in self.nodes:
            if node not in visited:
                if _dfs_cycle(node, None):
                    return True
        return False

    def is_tree(self) -> bool:
        if not self.nodes:
            return False
        return len(self.connected_components()) == 1 and not self.has_cycle()

    def is_bipartite(self) -> tuple[bool, dict[str, int]]:
        """
        Tests if the graph is bipartite using 2-coloring BFS.
        Returns (is_bipartite, color_map) where colors are 0 and 1.
        """
        color = {}
        for start_node in self.nodes:
            if start_node not in color:
                color[start_node] = 0
                queue = deque([start_node])
                while queue:
                    u = queue.popleft()
                    for v in self.adj[u]:
                        if v not in color:
                            color[v] = 1 - color[u]
                            queue.append(v)
                        elif color[v] == color[u]:
                            # Adjacent vertices share the same color -> odd cycle exists
                            return False, {}
        return True, color

    def visualize_to_html(self, filename: str = "graph_visualization.html", open_browser: bool = True):
        from pyvis.network import Network

        net = Network(
            height="760px",
            width="100%",
            bgcolor="#0b0f19",
            font_color="#00f3ff",
            directed=self.directed
        )

        degrees = {node: len(self.adj[node]) for node in self.nodes}

        for node in sorted(self.nodes):
            deg = degrees[node]
            size = 24 + (deg * 4)
            neighbors_str = ", ".join(sorted(self.adj[node]))
            tooltip = f"Vertex {node}\nDegree: {deg}\nNeighbors: [{neighbors_str}]"

            net.add_node(
                node,
                label=f" {node} ",
                title=tooltip,
                size=size,
                shape="dot",
                color={
                    "background": "#00f3ff",
                    "border": "#ff007f",
                    "highlight": {"background": "#39ff14", "border": "#ffffff"},
                    "hover": {"background": "#ffe600", "border": "#ff007f"}
                },
                borderWidth=3,
                shadow={
                    "enabled": True,
                    "color": "rgba(0, 243, 255, 0.6)",
                    "size": 20,
                    "x": 0,
                    "y": 0
                }
            )

        for u, v in self.edges:
            net.add_edge(
                u,
                v,
                color={"color": "rgba(255, 0, 127, 0.55)", "highlight": "#00f3ff", "hover": "#39ff14"},
                width=2.5,
                smooth={"type": "continuous", "roundness": 0.25}
            )

        net.set_options("""
        var options = {
          "nodes": {
            "font": { "size": 16, "face": "'JetBrains Mono', 'Courier New', monospace", "color": "#00f3ff", "bold": true }
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -3800,
              "centralGravity": 0.15,
              "springLength": 110,
              "springConstant": 0.05,
              "damping": 0.09
            },
            "stabilization": { "iterations": 180 }
          },
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "zoomView": true
          }
        }
        """)

        net.write_html(filename)

        custom_styles_and_hud = """
        <style>
            div.vis-tooltip {
                position: absolute;
                background: rgba(15, 23, 42, 0.95) !important;
                color: #00f3ff !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 13px !important;
                line-height: 1.5 !important;
                border: 1px solid #00f3ff !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                box-shadow: 0 0 15px rgba(0, 243, 255, 0.4) !important;
                white-space: pre-line !important;
                pointer-events: none;
                z-index: 10000;
            }
        </style>
        <div style="position: absolute; top: 18px; left: 20px; z-index: 999; font-family: 'JetBrains Mono', monospace; background: rgba(11, 15, 25, 0.85); backdrop-filter: blur(10px); padding: 14px 20px; border-radius: 10px; border: 1px solid #00f3ff; box-shadow: 0 0 15px rgba(0, 243, 255, 0.35);">
            <div style="font-weight: 800; font-size: 14px; color: #00f3ff; text-transform: uppercase; letter-spacing: 1.5px; display: flex; align-items: center; gap: 8px;">
                <span style="display:inline-block; width:8px; height:8px; background:#ff007f; border-radius:50%; box-shadow: 0 0 8px #ff007f;"></span>
                Discrete Graph Engine // Cyber-HUD
            </div>
            <div style="font-size: 11px; color: #8e9ebb; margin-top: 5px;">Drag vertices • Hover for connection metrics</div>
        </div>
        """

        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = html_content.replace("<body>", f"<body>\n{custom_styles_and_hud}")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open("file://" + os.path.realpath(filename))
        return filename
