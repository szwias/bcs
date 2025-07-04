# czlonkowie/management/commands/render_tree.py
from collections import defaultdict

from django.core.management.base import BaseCommand

from core.utils.Choices import TextChoose, IntAlt, TextAlt
from core.utils.czas.Czas import ROK_ZALOZENIA, BIEZACY_ROK
from czlonkowie.models import Czlonek
from drzewo.tree_rendering import render_layered_graph  # your helper

class Command(BaseCommand):
    help = "Render the pseudo‑genealogical tree from live DB data"

    def handle(self, *args, **options):
        layers, edges = build_layers_and_edges_from_db()
        # render_layered_graph(layers, edges, filename="tree.png")
        # self.stdout.write(self.style.SUCCESS("Tree rendered ➜ tree.png"))

def build_layers_and_edges_from_db():
    layers = {rocznik: [set()] for rocznik in range(ROK_ZALOZENIA, BIEZACY_ROK + 1)}
    edges = {}
    czlonkowie = Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]).select_related("rodzic_1", "rodzic_2")
    dzieci_czapki = []

    return layers, edges

def rodzic_is_unknown(rodzic):
    # Skip the sentinel “Nie wiem” object
    return rodzic.imie == "Nie" and rodzic.nazwisko == "wiem"

def rodzic_is_sentinel_value(rodzic):
    return rodzic.imie in {"Nie"} and rodzic.nazwisko in {"wiem", "dotyczy"}

def is_a_parent_of(parent, child):
    return parent.id in {child.rodzic_1, child.rodzic_2}
