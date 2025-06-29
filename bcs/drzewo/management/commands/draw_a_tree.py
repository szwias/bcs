# czlonkowie/management/commands/render_tree.py
from django.core.management.base import BaseCommand

from core.utils.Choices import TextChoose
from czlonkowie.models import Czlonek
from drzewo.tree_rendering import render_layered_graph  # your helper

class Command(BaseCommand):
    help = "Render the pseudo‑genealogical tree from live DB data"

    def handle(self, *args, **options):
        layers, edges = build_layers_and_edges_from_db()
        render_layered_graph(layers, edges, filename="tree.png")
        self.stdout.write(self.style.SUCCESS("Tree rendered ➜ tree.png"))

def build_layers_and_edges_from_db():
    """Translate Czlonek objects into the `layers` & `edges` structures"""
    layers = {}
    edges = {}
    czlonkowie = Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]).select_related("rodzic_1", "rodzic_2")

    for cz in czlonkowie:
        rok = cz.staz
        layers.setdefault(rok, []).append(cz.imie_piwne_1 or str(cz))

        for rodzic in (cz.rodzic_1, cz.rodzic_2):
            if rodzic and rodzic_id_is_real(rodzic):
                edges.setdefault(rodzic.imie_piwne_1 or str(rodzic), []).append(
                    cz.imie_piwne_1 or str(cz)
                )
    return layers, edges

def rodzic_id_is_real(rodzic):
    # Skip the sentinel “Nie wiem” / “Nie dotyczy” objects
    return rodzic.imie not in {"Nie"} and rodzic.nazwisko not in {"wiem", "dotyczy"}
