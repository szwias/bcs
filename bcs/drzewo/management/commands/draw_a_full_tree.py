# czlonkowie/management/commands/render_tree.py
from collections import defaultdict
import json

from django.core.management.base import BaseCommand

from core.utils.Choices import TextChoose, IntAlt
from core.utils.czas.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from czlonkowie.models import Czlonek
from drzewo.tree_rendering import render_layered_graph  # my helper
from drzewo.management.essentials import modify_layers_structure

class Command(BaseCommand):
    help = "Render the pseudo‑genealogical tree from live DB data"

    def handle(self, *args, **options):
        layers, edges, helper_dict = build_layers_and_edges_from_db()
        render_layered_graph(layers, edges, filename="tree.png")
        self.stdout.write(self.style.SUCCESS("Tree rendered ➜ tree.png"))
        for i in range(1, 5, 1):
            render_layered_graph(layers, edges, filename=f"tree_{i}.png")
            self.stdout.write(self.style.SUCCESS(f"Tree rendered ➜ tree_{i}.png"))


def build_layers_and_edges_from_db():
    layers = {rocznik: [set()] for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)}
    edges = {}
    helper_dict = defaultdict(lambda: [[], []])
    go = 1

    members = list(Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]))
    stack = []

    while members:
        if go == 1:
            stack.append(Node(Czlonek.objects.get(imie="Zdzisław", nazwisko="Gajda"), 0))
        elif go == 2:
            stack.append(Node(Czlonek.get_dont_know_czlonek(), 0))
        else:
            member = members.pop(0)
            if set(member.get_parents) & set(members):
                members.append(member)
                continue
            else:
                stack.append(Node(member, 2, 2))

        while stack:
            node = stack.pop()
            if node.member in members:
                members.remove(node.member)
            depth = node.depth
            layer = node.layer
            year = node.year
            member = node.member
            paczek = node.paczek # support dla ludzi, którzy "wypączkowali"

            while len(layers[year]) <= layer:
                layers[year].append(set())
            layers[year][layer].add(str(member))
            helper_dict[str(member)][0].append(f"{year}_{layer}")

            children = node.get_children()
            baptised_children = [c for c in children if c.ochrzczony == TextChoose.YES[0]]
            step_children = node.get_step_children()
            baptised_step_children = [sc for sc in step_children if sc.ochrzczony == TextChoose.YES[0]]

            for child in reversed(baptised_children):  # reversed to keep order similar to recursion
                if paczek:
                    if child == member:
                        continue
                stack.append((Node(child, depth + 1, layer)))
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
        new_dict[key].append(helper_dict[key])

    return modify_layers_structure(layers), edges, new_dict


class Node:
    def __init__(self, member, depth, parent_layer=0):
        self.member = member
        self.depth = depth
        self.parent_layer = parent_layer
        self.year = self.get_year()
        self.paczek = False
        self.youngest_parent = self.get_youngest_parent()
        self.layer = self.get_layer()

    def get_year(self):
        year = self.member.rok_chrztu if self.member.rok_chrztu != IntAlt.DONT_KNOW[0] else self.member.staz
        if year == IntAlt.DONT_KNOW[0]:
            if self.member.rodzic_2 == Czlonek.get_not_applicable_czlonek():
                year = Node(self.member.rodzic_1, self.depth - 1, self.parent_layer).get_year()
            else:
                year = Node(self.member.rodzic_2, self.depth - 1, self.parent_layer).get_year()
        return year

    def get_youngest_parent(self):
        if self.member.rodzic_2 != Czlonek.get_not_applicable_czlonek():
            return self.member.rodzic_2
        if self.member.rodzic_1 == self.member:
            self.paczek = True
            self.depth = 0
        return self.member.rodzic_1

    def get_layer(self):
        if not self.depth:
            return 0
        if self.depth == 1 or self.year == Node(self.youngest_parent, self.depth - 1, self.parent_layer).get_year():
            return self.parent_layer + 1
        return 0

    def get_children(self):
        return self.member.dzieci_pierwszy_wybor.all()

    def get_step_children(self):
        return self.member.dzieci_drugi_wybor.all()
