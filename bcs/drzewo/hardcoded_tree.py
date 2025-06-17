from tree_rendering import *

layers = {
    # 2009
    1: ["Profesor", ],
    2: ["Jakub Nawrot", "Kamila Rozesłaniec", "Pumba", "Michał Lenik", "Paweł Nawrot", "Tadek", "Urszula Kasprzyk", "Małgorzata Żurek", ],
    3: ["Czapka", ],
    4: ["Małgorzata Lurzyńska", ],
    # 2010
    5: ["Gujda", "Astel", "Geolog", "Kasztanka", ],
    6: ["Aśka", ],
    # 2011
    7: ["Avis", "Aleksander Wędrychowski", "Gestapo", "Biba", "Artur Miadzielec", "Maciej Hyla", "Martinus", "Piotr Bulica", "Roksana Kidawa", "Estel", ],
    8: ["Artur Halcarz", "Szparag", "Benikaza", "Wawrzyn", ],
    9: ["Synek", ],
    # 2012
    10: ["Jezus", "Paula Dybowska", ],
    11: ["Aneta Galara", ],
    # 2013
    12: ["Stefan Pierwszy Płaszcz Gondoru", "Potomek", ],
    # 2014
    13: ["Dziadek", "Abeille", "Hipster", "Poronny Panicz", "Cami", "Karolina Szklanny", "Poniatowski", "Solon", "Paulina Malinowska-Majdak", "Przemysław Jankowski", "Sigurd", "Wacław Chmiel", ],
    14: ["Bisquit", ],
    # 2015
    15: ["Paulina Tomżyńska", "Benio", "Bandera", "Eryk", "Gabriela Michalik (Mucha)", "Cybuch", "Dzidzia", "Rysia", "Koala", "Lewe Jądro w Ciemności", ],
    # 2016
    16: ["Księżniczka_1", "Mała Ania", "Ciepły", "Pryk", "Cezary Sołtysek", "Malina", "Natalia Stachura", "Dżdżysław", ],
    # 2017
    17: ["Księżniczka_2", "Krwawa Baronessa", "Max", "Deanus", "Manista", ],
    # 2018
    18: ["Rana", "Emalia", "Dar Szczecina", "Kucharz", "Doris", "Sułtan", "Gomuł", "Monia", "Chat", ],
    # 2019
    19: ["Adrenalina", "Ada z penisem", "Jasiek", "Katarzyna Marek", "Mmm...", "Śnięty Cwel Kacper", "Szynka", "Hrabina", "Koziołek", "Prawnik", ],
    # 2020
    20: ["Kotlet", ],
    # 2022
    21: ["Bezimienna", "Lis", ],
    # 2023
    22: ["Nobod", "Szanciarz", "Księciunio", "Malata", ],
    # 2024
    23: ["Heniek", "Rakieta", "Felis", "Bober", "Allec", "Equus", "Sander", ],
    # 2025
    24: ["Rudy", "Jeżyk", "Chłopiec z Warszawy", "Artifex", "Marchewa", ],
}

edges = {
    "Profesor": ["Jakub Nawrot", "Kamila Rozesłaniec", "Pumba", "Michał Lenik", "Paweł Nawrot", "Małgorzata Żurek", "Tadek", "Urszula Kasprzyk", ],
    "Tadek": ["Czapka", "Gujda", "Astel", "Geolog", "Kasztanka", "Roksana Kidawa", "Benio", "Cybuch", "Manista", "Szynka", ],
    "Pumba": ["Czapka", ],
    "Czapka": ["Małgorzata Lurzyńska", "Aleksander Wędrychowski", "Maciej Hyla", "Martinus", "Piotr Bulica", "Estel", "Eryk", "Księżniczka_1", "Natalia Stachura", ],
    "Gujda": ["Aśka", "Avis", "Sigurd", "Dżdżysław", ],
    "Geolog": ["Gestapo", "Artur Miadzielec", "Abeille", ],
    "Kasztanka": ["Biba", "Jezus", "Paula Dybowska", "Hipster", "Poronny Panicz", "Wacław Chmiel", ],
    "Gestapo": ["Artur Halcarz", "Szparag", "Benikaza", "Wawrzyn", "Stefan Pierwszy Płaszcz Gondoru", "Potomek", "Przemysław Jankowski", "Malina", ],
    "Szparag": ["Synek", ],
    "Jezus": ["Aneta Galara", "Poniatowski", "Gabriela Michalik (Mucha)", "Rysia", "Pryk", ],
    "Paula Dybowska": ["Dziadek", ],
    "Estel": ["Cami", "Paulina Malinowska-Majdak", "Gabriela Michalik (Mucha)", ],
    "Stefan Pierwszy Płaszcz Gondoru": ["Karolina Szklanny", "Koala", ],
    "Avis": ["Solon", ],
    "Abeille": ["Paulina Tomżyńska", ],
    "Paulina Malinowska-Majdak": ["Bisquit", ],
    "Bisquit": ["Bandera", "Chat", ],
    "Synek": ["Dzidzia", "Krwawa Baronessa", ],
    "Koala": ["Mała Ania", "Kotlet", ],
    "Dzidzia": ["Ciepły", ],
    "Solon": ["Lewe Jądro w Ciemności", "Cezary Sołtysek", ],
    "Pryk": ["Deanus", "Emalia", "Kucharz", "Sułtan", ],
    "Lewe Jądro w Ciemności": ["Księżniczka_2", "Max", ],
    "Bandera": ["Dar Szczecina", "Doris", "Gomuł", "Mmm...", "Koziołek", ],
    "Deanus": ["Rana", ],
    "Natalia Stachura": ["Kucharz", ],
    "Krwawa Baronessa": ["Gomuł", ],
    "Manista": ["Monia", "Chat", ],
    "Gomuł": ["Adrenalina", "Ada z penisem", "Jasiek", "Hrabina", "Prawnik", "Bezimienna", ],
    "Doris": ["Katarzyna Marek", ],
    "Chat": ["Śnięty Cwel Kacper", ],
    "Koziołek": ["Lis", "Artifex", ],
    "Kotlet": ["Nobod", "Szanciarz", ],
    "Rana": ["Księciunio", "Felis", "Allec", "Equus" ],
    "Jasiek": ["Malata", ],
    "Lis": ["Malata", ],
    "Kucharz": ["Heniek", ],
    "Nobod": ["Rakieta", "Sander", ],
    "Malata": ["Bober", ],
    "Monia": ["Rudy", ],
    "Rakieta": ["Jeżyk", ],
    "Heniek": ["Chłopiec z Warszawy", ],
    "Szynka": ["Marchewa", ],
}

# color_groups = {
#     "red": ["Tadek", "Kasztanka", "Synek", "Dzidzia", "Bandera", "Kucharz", "Jasiek", "Koziołek", "Malata", ],
#     "green": ["Pumba", "Gestapo", "Roksana Kidawa", "Jezus", "Koala", "Manista", "Prawnik", "Jezus", "Nobod", ],
#     "gold": ["Urszula Kasprzyk", "Abeille", "Paulina Tomżyńska", "Natalia Stachura", "Dar Szczecina", "Bober", ],
#     "brown": ["Michał Lenik", "Geolog", "Biba", "Sigurd", "Solon", "Pryk", "Krwawa Baronessa", "Kotlet", "Szanciarz", "Heniek", ],
#     "silver": ["Stefan Pierwszy Płaszcz Gondoru", "Paula Dybowska", "Gujda", "Ciepły", "Rana", "Lis", "Księciunio", ],
# }
#
# node_attrs = build_node_attrs_from_colors(color_groups)

render_layered_graph(
    layers, edges, filename="tree.png",
    # node_attrs=node_attrs
)