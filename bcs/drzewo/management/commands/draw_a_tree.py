# czlonkowie/management/commands/render_tree.py
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError

from core.utils.Choices import TextChoose
from core.utils.czas.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from czlonkowie.models import Czlonek
from drzewo.management.utils.tree_rendering import render_layered_graph  # my helper
from drzewo.management.utils.essentials import modify_layers_structure, TreeNode

class Command(BaseCommand):
    help = 'Builds a tree with configurable scope'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layers = {}
        self.edges = {}
        self.scoped_layers = {}
        self.scoped_edges = {}
        self.helper_dict = {}
        self.member_id = 0
        self.member = None
        self.depth = 0
        self.gen = 0

    def add_arguments(self, parser):
        parser.add_argument(
            'tree_scope',
            choices=['full', 'limited'],
            help='Possible scopes: "full", "limited"'
        )
        parser.add_argument(
            '--member_id',
            type=str,
            help='Member ID (required if scope is "limited")'
        )
        parser.add_argument(
            '--depth',
            type=int,
            help='Branches depth (required if scope is "limited")'
        )
        parser.add_argument(
            '--gen',
            type=int,
            default=3 * (BIEZACY_ROK - ROK_ZALOZENIA + 1),
            help='Number of generations'
        )

    def handle(self, *args, **options):
        scope = options['tree_scope']
        self.member_id = options.get('member_id')
        self.depth = options.get('depth')
        self.gen = options.get('gen')

        if scope == 'limited':
            if not self.member_id or self.depth is None:
                raise CommandError('For "limited" scope, both --member_id and --depth must be provided.')
            try:
                self.member = Czlonek.objects.get(id=self.member_id)
            except Czlonek.DoesNotExist:
                raise CommandError(f"Czlonek with id {self.member_id} does not exist.")
            self.stdout.write(f"Building limited tree for member {str(self.member)} with depth={self.depth}")
        else:
            self.stdout.write("Building full tree")

        self.layers, self.edges, self.helper_dict = self.build_layers_and_edges_from_db()

        if scope == "limited":
            self.generate_scoped_tree()
        else:
            self.generate_full_tree()

    def generate_full_tree(self):
        render_layered_graph(self.layers, self.edges,
            path="/home/szymon/Desktop/bcs/bcs/drzewo/management/trees/full_tree.png")
        self.stdout.write(self.style.SUCCESS("Tree rendered ➜ full_tree.png"))

    def generate_scoped_tree(self):
        self.build_scoped_layers_and_edges()
        title = f"tree_{self.member_id}_depth_{self.depth}_gen_{self.gen}"
        render_layered_graph(self.scoped_layers, self.scoped_edges,
            path=f"/home/szymon/Desktop/bcs/bcs/drzewo/management/trees/{title}.png")
        self.stdout.write(self.style.SUCCESS(f"Tree rendered ➜ {title}.png"))

    def build_scoped_layers_and_edges(self):
        stack = [(self.member, 0, 1)]

        while stack:
            member, depth, gen = stack.pop()
            str_member = str(member)

            layer = self.helper_dict[str_member][0]
            self.scoped_layers.setdefault(layer, []).append(str_member)

            if gen < self.gen and not depth:
                parents = member.get_parents()
                for parent in parents:
                    self.scoped_edges.setdefault(parent, []).append(str_member)
                    stack.append((parent, depth, gen + 1))

            children = self.helper_dict[str_member][1]
            for ch in children:
                if depth < self.depth:
                    self.scoped_edges.setdefault(str_member, []).append(str(ch))
                    stack.append((ch, depth + 1, gen - 1))

    @staticmethod
    def build_layers_and_edges_from_db():
        layers = {rocznik: [set()] for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)}
        edges = {}
        helper_dict = defaultdict(lambda: [None, []])
        go = 1

        members = list(Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]))
        stack = []

        while members:
            if go == 1:
                stack.append(TreeNode(Czlonek.objects.get(imie="Zdzisław", nazwisko="Gajda"), 0))
            elif go == 2:
                stack.append(TreeNode(Czlonek.get_dont_know_czlonek(), 0))
            else:
                member = members.pop(0)
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
