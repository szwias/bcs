from collections import defaultdict

def modify_layers_structure(layers):
    new_layers = defaultdict(list)
    for year in layers:
        for layer, contents in enumerate(layers[year]):
            new_layers[f"{year}_{layer}"].extend(contents)

    return new_layers

def is_sentinel(member):
    return member.imie == "Nie" and member.nazwisko == "wiem"

def exists(member):
    return not (member.imie == "Nie" and member.nazwisko == "dotyczy")

def str_repr(member):
    return "Czapka" if is_sentinel(member) else str(member)