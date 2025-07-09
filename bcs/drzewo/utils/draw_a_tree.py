# czlonkowie/management/commands/draw_a_tree.py
from collections import defaultdict
from core.utils.Choices import TextChoose
from core.utils.czas.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from czlonkowie.models import Czlonek
from drzewo.utils.tree_rendering import render_layered_graph  # my helper
from drzewo.utils.essentials import modify_layers_structure, TreeNode

def generate_full_tree(path, onp=False):
    layers, edges, helper_dict = build_layers_and_edges_from_db(onp)
    render_layered_graph(layers, edges, path)

def generate_scoped_tree(path, member, depth, gen):
    _, _, helper_dict = build_layers_and_edges_from_db()
    layers, edges = build_scoped_layers_and_edges(member, depth, gen, helper_dict)
    render_layered_graph(layers, edges,path)

def build_scoped_layers_and_edges(member, depth, gen, helper_dict):
    layers = {}
    edges = {}

    stack = [(member, 0, 1)]

    while stack:
        c_member, c_depth, c_gen = stack.pop()
        str_member = str(c_member)

        layer = helper_dict[str_member][0]
        layers.setdefault(layer, []).append(str_member)

        if c_gen < gen and not c_depth:
            parents = c_member.get_parents()
            for parent in parents:
                edges.setdefault(parent, []).append(str_member)
                stack.append((parent, c_depth, c_gen + 1))

        children = helper_dict[str_member][1]
        for ch in children:
            if c_depth < depth:
                edges.setdefault(str_member, []).append(str(ch))
                stack.append((ch, c_depth + 1, c_gen - 1))

    return layers, edges

def build_layers_and_edges_from_db(onp):
    layers = {rocznik: [set()] for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)}
    print(f"DuPA: {onp}")
    edges = {}
    helper_dict = defaultdict(lambda: [None, []])
    go = 1

    members = list(Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]))
    if onp:
        members.remove(Czlonek.get_dont_know_czlonek())
    stack = []

    while members:
        print(members)
        if go == 1:
            stack.append(TreeNode(Czlonek.objects.get(imie="Zdzisław", nazwisko="Gajda"), 0))
        elif go == 2 and not onp:
            stack.append(TreeNode(Czlonek.get_dont_know_czlonek(), 0))
        else:
            member = members.pop(0)
            if onp and member.rodzic_1.is_unknown():
                continue
            if set(member.get_parents()) & set(members):
                members.append(member)
                continue
            else:
                stack.append(TreeNode(member, 2, 2))

        while stack:
            node = stack.pop()
            if node.member in members:
                members.remove(node.member)
            depth = node.depth
            layer = node.layer
            year = node.year
            member = node.member
            print(str(member))
            paczek = node.paczek # support dla ludzi, którzy "wypączkowali"

            while len(layers[year]) <= layer:
                layers[year].append(set())
            layers[year][layer].add(str(member))
            helper_dict[str(member)][0] = f"{year}_{layer}"

            children = member.get_children()
            baptised_children = [c for c in children if c.ochrzczony == TextChoose.YES[0]]
            step_children = member.get_step_children()
            baptised_step_children = [sc for sc in step_children if sc.ochrzczony == TextChoose.YES[0]]

            for child in reversed(baptised_children):  # reversed to keep order similar to recursion
                if paczek:
                    if child == member:
                        continue
                stack.append((TreeNode(child, depth + 1, layer)))
                edges.setdefault(str(member), []).append(str(child))
                helper_dict[str(member)][1].append(str(child))

            for step_child in baptised_step_children:
                edges.setdefault(str(member), []).append(str(step_child))
                helper_dict[str(member)][1].append(str(step_child))

        members.sort(key=lambda x: x.staz)
        go += 1

    new_dict = defaultdict(list)
    sorted_keys = sorted(helper_dict.keys())
    for key in sorted_keys:
        new_dict[key] = helper_dict[key]

    return modify_layers_structure(layers), edges, new_dict
