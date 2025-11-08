import pygraphviz as pgv
from django.http import JsonResponse

DUMMY_PREFIX = "__layer_anchor__"

def render_layered_graph(layers, edges, rankdir="TB", node_attrs=None):
    G = pgv.AGraph(strict=True, directed=True)
    G.graph_attr.update(rankdir=rankdir)

    node_attrs = node_attrs or {}
    sorted_layers = sorted(layers.items())

    for layer_num, nodes in sorted_layers:
        dummy = f"{DUMMY_PREFIX}{layer_num}"
        G.add_node(n=dummy, style="invis", width=0, height=0)

        for node in nodes:
            attrs = node_attrs.get(node, {})
            G.add_node(n=node, **attrs)

        G.add_subgraph(nbunch=list(nodes) + [dummy], rank="same")

    # Edges
    for src, targets in edges.items():
        for dst in targets:
            G.add_edge(u=src, v=dst)

    # Enforce vertical ordering with invisible anchors
    for i in range(len(sorted_layers) - 1):
        current_nodes = sorted_layers[i][1]
        next_dummy = f"{DUMMY_PREFIX}{sorted_layers[i + 1][0]}"
        if current_nodes:
            G.add_edge(u=current_nodes[0], v=next_dummy, style="invis")

    G.layout(prog="dot")
    return G

def build_d3_coords(graph):
    G = graph.copy()
    # Extract positions and build JSON objects for real nodes only
    node_positions = {}
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")

    for n in G.nodes():
        name = n.get_name()
        if name.startswith(DUMMY_PREFIX):
            continue
        pos = n.attr.get("pos")
        if not pos:
            # fallback: skip or set to (0,0)
            continue
        # pos is "x,y" (strings), sometimes with extra formatting; parse
        try:
            x_str, y_str = pos.split(",")
            x = float(x_str)
            y = float(y_str)
        except Exception:
            # try other patterns or skip
            continue

        # track bounds for normalization later
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        node_positions[name] = {
            "id": name,
            "name": name,
            "x": x,
            "y": y,
            "color": "#88c",
        }

    # Build links (keep only links whose endpoints are real nodes)
    links_out = []
    for e in G.edges():
        src = e[0]
        dst = e[1]
        # skip edges involving dummy anchors
        if str(src).startswith(DUMMY_PREFIX) or str(dst).startswith(
            DUMMY_PREFIX
        ):
            continue
        if src in node_positions and dst in node_positions:
            links_out.append({"source": str(src), "target": str(dst)})

    # Normalize coordinates to a reasonable viewport (optional)
    # Create a padding and scale so everything fits in e.g. 2000x2000 coordinate space
    PAD = 50
    width_target = 2000
    height_target = 2000
    bbox_w = max_x - min_x if max_x > min_x else 1
    bbox_h = max_y - min_y if max_y > min_y else 1
    sx = (width_target - 2 * PAD) / bbox_w
    sy = (height_target - 2 * PAD) / bbox_h
    s = min(sx, sy)

    # Flip Y (Graphviz y=0 is bottom?) — Graphviz coords usually have origin bottom-left,
    # while browser SVG has origin top-left. We'll flip to match visual expectation.
    for ndata in node_positions.values():
        ndata["x_norm"] = (ndata["x"] - min_x) * s + PAD
        # flip y
        ndata["y_norm"] = (max_y - ndata["y"]) * s + PAD

    nodes_out = list(node_positions.values())

    return JsonResponse({"nodes": nodes_out, "links": links_out})


def build_node_attrs_from_colors(color_groups):
    node_attrs = {}
    for color, nodes in color_groups.items():
        for node in nodes:
            node_attrs[node] = {
                "fillcolor": color,
                "style": "filled",
                "shape": "ellipse",
            }
    return node_attrs
