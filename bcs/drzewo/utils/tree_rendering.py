import pygraphviz as pgv
from django.forms import model_to_dict
from django.http import JsonResponse

DUMMY_PREFIX = "__layer_anchor__"
DEFAULT_NODE_WIDTH = 0.5


def render_layered_graph(layers, edges, rankdir="TB", node_attrs=None):
    G = pgv.AGraph(strict=True, directed=True)
    G.graph_attr.update(rankdir=rankdir)
    G.graph_attr.update(ranksep="1.6")

    node_attrs = node_attrs or {}
    sorted_layers = sorted(layers.items())
    pk_to_name_dict = {}

    for layer_num, members in sorted_layers:
        dummy = f"{DUMMY_PREFIX}{layer_num}"
        G.add_node(n=dummy, style="invis", width=0, height=0)

        for m in members:
            name = str(m)
            passed_attrs = node_attrs.get(name, {})
            attrs = model_to_dict(m)
            attrs.update(**passed_attrs)

            pk = m.pk
            attrs["pk"] = pk
            pk_to_name_dict[pk] = name

            attrs["layer"] = layer_num
            attrs["year"] = layer_num[:4]

            attrs["parent1"] = str(m.rodzic_1)
            attrs["parent2"] = str(m.rodzic_2)

            G.add_node(n=name, **attrs)

        G.add_subgraph(nbunch=list(members) + [dummy], rank="same")

    # Edges
    for (src, target), parent_type in edges.items():
        src = pk_to_name_dict[src]
        dest = pk_to_name_dict[target]
        edge_type = "full" if parent_type == "final_parent" else "dashed"
        G.add_edge(u=src, v=dest, type=edge_type)

    # Enforce vertical ordering with invisible anchors
    for i in range(len(sorted_layers) - 1):
        current_nodes = sorted_layers[i][1]
        next_dummy = f"{DUMMY_PREFIX}{sorted_layers[i + 1][0]}"
        if current_nodes:
            G.add_edge(u=str(current_nodes[0]), v=next_dummy, style="invis")

    G.layout(prog="dot")
    return G


def build_d3_nodes(graph, year_reprs, children_dict, node_size=0.5):
    POINTS_IN_AN_INCH = 72
    G = graph.copy()
    ranksep = G.graph_attr["ranksep"]

    # Extract positions and build JSON objects for real nodes only
    node_positions = {}
    node_attrs = {}
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")

    for n in G.nodes():
        name = n.get_name()
        if name.startswith(DUMMY_PREFIX):
            continue
        pos = n.attr.get("pos")
        if not pos:
            continue

        x, y = map(float, pos.split(","))
        width = float(n.attr.get("width", node_size)) * POINTS_IN_AN_INCH
        height = float(n.attr.get("height", node_size)) * POINTS_IN_AN_INCH
        node_attrs[name] = n.attr

        # track bounds for normalization later
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        node_positions[name] = {
            **n.attr,
            "id": name,
            "name": name,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "color": n.attr.get("fillcolor", "#66aaff"),
        }

    # Build links (keep only links whose endpoints are real nodes)
    links_out = []
    for e in G.edges():
        src = e[0]
        dst = e[1]
        edge_type = e.attr.get("type", "full")
        # skip edges involving dummy anchors
        if str(src).startswith(DUMMY_PREFIX) or str(dst).startswith(
            DUMMY_PREFIX
        ):
            continue
        if src in node_positions and dst in node_positions:
            links_out.append(
                {"source": str(src), "target": str(dst), "type": edge_type}
            )

    # Flip Y (Graphviz y=0 is bottom?) — Graphviz coords usually have origin bottom-left,
    # while browser SVG has origin top-left. We'll flip to match visual expectation.
    for ndata in node_positions.values():
        ndata["x_norm"] = ndata["x"] - min_x
        # flip y
        ndata["y_norm"] = max_y - ndata["y"]

    nodes_out = list(node_positions.values())
    return JsonResponse(
        {
            "nodes": nodes_out,
            "links": links_out,
            "years": year_reprs,
            "childrenDict": children_dict,
            "layerDistance": float(ranksep) * POINTS_IN_AN_INCH,
        }
    )


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
