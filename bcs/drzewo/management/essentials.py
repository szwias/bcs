from collections import defaultdict

def modify_layers_structure(layers):
    new_layers = defaultdict(list)
    for year in layers:
        for layer, contents in enumerate(layers[year]):
            new_layers[f"{year}_{layer}"].extend(contents)

    return new_layers