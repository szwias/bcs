# osoby/management/commands/draw_a_tree.py
from collections import defaultdict

from core.utils.Choices import TextChoose
from core.utils.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from osoby.models import Czlonek, Bean
from drzewo.utils.tree_rendering import render_layered_graph  # my helper
from drzewo.utils.essentials import modify_layers_structure, TreeNode


def generate_full_tree(path, onp):
    layers, edges, children_dict, _ = build_layers_and_edges_from_db(onp)
    G = render_layered_graph(layers=layers, edges=edges)
    G.draw(path=path)


def generate_scoped_tree(path, member, depth, gen, onp):
    _, _, children_dict, _ = build_layers_and_edges_from_db(onp)
    layers, edges = build_scoped_layers_and_edges(
        member=member,
        depth=depth,
        gen=gen,
        onp=onp,
        children_dict=children_dict,
    )
    G = render_layered_graph(
        layers=layers,
        edges=edges,
        node_attrs={
            str(member): {
                "fillcolor": "green",
                "style": "filled",
                "shape": "ellipse",
            }
        },
    )
    G.draw(path=path)


def build_scoped_layers_and_edges(member, depth, gen, onp, children_dict):
    layers = {}
    edges = {}

    stack = [(member, 0, 1)]

    while stack:
        c_member, c_depth, c_gen = stack.pop()
        member_pk = c_member.pk
        str_member = str(c_member)

        if onp and member_pk not in children_dict.keys():
            layer = f"{ROK_ZALOZENIA}_1"
        else:
            layer = children_dict[member_pk][0]
        layers.setdefault(layer, []).append(c_member)

        if c_gen < gen and not c_depth:
            parents = c_member.get_parents()
            for parent in parents:
                if onp and parent.is_unknown():
                    pass
                else:
                    edges.setdefault(parent, []).append(str_member)
                    stack.append((parent, c_depth, c_gen + 1))

        if onp and member_pk not in children_dict.keys():
            children = (
                c_member.get_member_children()
                + c_member.get_member_step_children()
            )
        else:
            children = {
                Czlonek.objects.get(pk=_pk)
                for _pk in children_dict[member_pk][1]
            }
        for ch in children:
            if c_depth < depth:
                edges.setdefault(str_member, []).append(str(ch))
                stack.append((ch, c_depth + 1, c_gen - 1))

    return layers, edges


def build_layers_and_edges_from_db(onp, beans):
    layers = {
        str(rocznik): [set()]
        for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)
    }
    if beans:
        layers["BEAN"] = [set()]
    edges = {}
    children_dict = defaultdict(lambda: [None, []])
    abandons = {}
    go = 1

    members = list(
        Czlonek.objects.filter(archiwum=False).filter(
            ochrzczony=TextChoose.YES[0]
        )
    )
    if beans:
        allBeans = Bean.objects.all()
        beans_with_parents = set(allBeans) - set(
            allBeans.filter(rodzic_1=Czlonek.get_not_applicable_czlonek())
        )
        members += list(beans_with_parents)
    if onp:
        members.remove(Czlonek.get_dont_know_czlonek())
    stack = []

    while members:
        if go == 1:
            stack.append(
                TreeNode(
                    member=Czlonek.objects.get(
                        imie="Zdzisław", nazwisko="Gajda"
                    ),
                    depth=0,
                )
            )
        elif go == 2 and not onp:
            stack.append(
                TreeNode(member=Czlonek.get_dont_know_czlonek(), depth=0)
            )
        else:
            member = members.pop(0)
            if onp and member.rodzic_1.is_unknown():
                continue
            if set(member.get_parents()) & set(members):
                continue
            else:
                stack.append(TreeNode(member=member, depth=2, parent_layer=2))

        while stack:
            node = stack.pop()
            if node.member in members:
                members.remove(node.member)
            depth = node.depth
            layer = node.layer
            year = node.year
            member = node.member
            if str(member) == "Natalia Stachura":
                print("WTF")
            paczek = node.paczek  # support dla ludzi, którzy "wypączkowali"

            if member.rodzic_2 != Czlonek.get_not_applicable_czlonek():
                abandons[member.pk] = member.rodzic_1.pk

            while len(layers[year]) <= layer:
                layers[year].append(set())
            layers[year][layer].add(member)

            if isinstance(member, Czlonek):
                children_dict[member.pk][0] = f"{year}_{layer}"

                children = member.get_member_children()
                baptised_children = [
                    c for c in children if c.ochrzczony == TextChoose.YES[0]
                ]
                if beans:
                    baptised_children += member.get_bean_children()
                step_children = member.get_member_step_children()
                baptised_step_children = [
                    sc
                    for sc in step_children
                    if sc.ochrzczony == TextChoose.YES[0]
                ]
                if beans:
                    baptised_step_children += member.get_bean_step_children()

                for child in reversed(
                    baptised_children
                ):  # reversed to keep order similar to recursion
                    if paczek:
                        if child == member:
                            continue
                    stack.append(
                        (
                            TreeNode(
                                member=child,
                                depth=depth + 1,
                                parent_layer=layer,
                            )
                        )
                    )
                    edges.setdefault((member.pk, child.pk), "final_parent")
                    children_dict[member.pk][1].append(child.pk)

                for step_child in baptised_step_children:
                    edges.setdefault(
                        (member.pk, step_child.pk), "final_parent"
                    )
                    children_dict[member.pk][1].append(step_child.pk)

        members.sort(key=lambda x: x.staz)
        go += 1

    for abandoned, parent1 in abandons.items():
        edges[(parent1, abandoned)] = "non_final_parent"

    new_dict = defaultdict(list)
    sorted_keys = sorted(children_dict.keys())
    for key in sorted_keys:
        new_dict[key] = children_dict[key]

    year_reprs = {}
    last_year_label = str(ROK_ZALOZENIA)
    for year, sub_layers in layers.items():
        label = str(year)
        if sub_layers[0] == set():
            new_label = last_year_label + ", " + label
            year_reprs[new_label] = year_reprs[last_year_label]
            del year_reprs[last_year_label]
            last_year_label = new_label
        else:
            year_reprs[label] = str(list(sub_layers[0])[0])
            last_year_label = label

    return modify_layers_structure(layers), edges, new_dict, year_reprs
