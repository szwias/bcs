from collections import defaultdict
from czlonkowie.models import OldCzlonek
from core.utils.Choices import IntAlt

def modify_layers_structure(layers):
    new_layers = defaultdict(list)
    for year in layers:
        for layer, contents in enumerate(layers[year]):
            new_layers[f"{year}_{layer}"].extend(contents)

    return new_layers

class TreeNode:
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
            if self.member.rodzic_2 == OldCzlonek.get_not_applicable_czlonek():
                year = TreeNode(self.member.rodzic_1, self.depth - 1, self.parent_layer).get_year()
            else:
                year = TreeNode(self.member.rodzic_2, self.depth - 1, self.parent_layer).get_year()
        return year

    def get_youngest_parent(self):
        if self.member.rodzic_2 != OldCzlonek.get_not_applicable_czlonek():
            return self.member.rodzic_2
        if self.member.rodzic_1 == self.member:
            self.paczek = True
            self.depth = 0
        return self.member.rodzic_1

    def get_layer(self):
        if not self.depth:
            return 0
        if self.depth == 1 or self.year == TreeNode(self.youngest_parent, self.depth - 1, self.parent_layer).get_year():
            return self.parent_layer + 1
        return 0
