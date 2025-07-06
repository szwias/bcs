# czlonkowie/management/commands/render_tree.py
from collections import defaultdict

from django.core.management.base import BaseCommand

from core.utils.Choices import TextChoose, IntAlt
from core.utils.czas.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from czlonkowie.models import Czlonek
from drzewo.tree_rendering import render_layered_graph  # my helper

class Command(BaseCommand):
    help = "Render the pseudo‑genealogical tree from live DB data"

    def handle(self, *args, **options):
        layers, edges = build_layers_and_edges_from_db()

        for i in range(1, 7, 1):
            render_layered_graph(layers, edges, filename=f"tree_{i}.png")
        self.stdout.write(self.style.SUCCESS("Tree rendered ➜ tree.png"))


def build_layers_and_edges_from_db():
    layers = {rocznik: [set()] for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)}
    edges = {}

    members = list(Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]))
    stack = [Node(Czlonek.objects.get(imie="Zdzisław", nazwisko="Gajda"), 0)]
    first_go_finished = False

    while members:
        if first_go_finished:
            stack.append(Node(members[0], 2, 2))
        while stack:
            node = stack.pop()
            if node.member in members:
                members.remove(node.member)
            depth = node.depth
            layer = node.layer
            year = node.year
            member = node.member
            if member.imie == "Szymon":
                print(str(member))
            paczek = node.paczek # support dla ludzi, którzy "wypączkowali"

            if paczek:
                edges.setdefault("Czapka", []).append(str_repr(member))

            while len(layers[year]) <= layer:
                layers[year].append(set())
            layers[year][layer].add(str_repr(member))

            children = node.get_children()
            baptised_children = [c for c in children if c.ochrzczony == TextChoose.YES[0]]
            step_children = node.get_step_children()
            baptised_step_children = [sc for sc in step_children if sc.ochrzczony == TextChoose.YES[0]]

            for child in reversed(baptised_children):  # reversed to keep order similar to recursion
                if paczek:
                    if child == member:
                        continue
                stack.append((Node(child, depth + 1, layer)))
                edges.setdefault(str_repr(member), []).append(str_repr(child))

            for step_child in baptised_step_children:
                edges.setdefault(str_repr(member), []).append(str_repr(step_child))

        first_go_finished = True

        members.sort(key=lambda x: x.staz)

    return modify_layers_structure(layers), edges

def modify_layers_structure(layers):
    new_layers = defaultdict(list)
    for year in layers:
        for layer, contents in enumerate(layers[year]):
            new_layers[f"{year}_{layer}"].extend(contents)

    return new_layers


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
            return Czlonek.get_dont_know_czlonek()
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

def is_sentinel(member):
    return member.imie == "Nie" and member.nazwisko == "wiem"

def str_repr(member):
    return "Czapka" if is_sentinel(member) else str(member)