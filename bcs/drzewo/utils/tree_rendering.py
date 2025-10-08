import pygraphviz as pgv


def render_layered_graph(layers, edges, path, rankdir="TB", node_attrs=None):
    G = pgv.AGraph(strict=True, directed=True)
    G.graph_attr.update(rankdir=rankdir)

    dummy_prefix = "__layer_anchor__"
    node_attrs = node_attrs or {}
    sorted_layers = sorted(layers.items())

    for layer_num, nodes in sorted_layers:
        dummy = f"{dummy_prefix}{layer_num}"
        G.add_node(n=dummy, style="invis", width=0, height=0)

        for node in nodes:
            attrs = node_attrs.get(node, {})
            G.add_node(n=node, **attrs)

        G.add_subgraph(nbunch=nodes + [dummy], rank="same")

    # Edges
    if isinstance(edges, dict):
        for src, targets in edges.items():
            for dst in targets:
                G.add_edge(u=src, v=dst)
    else:
        for src, dst in edges:
            G.add_edge(u=src, v=dst)

    # Enforce vertical ordering with invisible anchors
    for i in range(len(sorted_layers) - 1):
        current_nodes = sorted_layers[i][1]
        next_dummy = f"{dummy_prefix}{sorted_layers[i + 1][0]}"
        if current_nodes:
            G.add_edge(u=current_nodes[0], v=next_dummy, style="invis")

    G.layout(prog="dot")
    G.draw(path=path)


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
