from core.autocompletion.registry import register_autocomplete
autocomplete_urls, autocomplete_widgets = register_autocomplete(overrides={})

import json
from django.shortcuts import render, get_object_or_404
from .models import Piosenka

def piosenka(request, pk):
    song = get_object_or_404(Piosenka, pk=pk)

    lines = []
    if song.tekst:
        with song.tekst.open("r") as f:
            lines = json.load(f)

    formatted_lines = []
    lyrics = [line["tekst"] for line in lines]
    chords = [' '.join(line["chwyty"]) for line in lines]

    # Determine fixed right alignment
    max_lyrics_len = max((len(l) for l in lyrics), default=0)
    max_chords_len = max((len(c) for c in chords), default=0)
    right_border = max_lyrics_len + 4 + max_chords_len

    for l, c in zip(lyrics, chords):
        if not l and not c:
            formatted_lines.append("")  # blank line
            continue
        spaces_needed = right_border - len(l) - len(c)
        formatted_lines.append(l + ' ' * spaces_needed + c)

    if song.autor:
        author = f"Autor: {song.autor}"
    elif song.znani_czapce_autorzy:
        autorzy = list(song.znani_czapce_autorzy.all())
        start = "Autorzy" if len(autorzy) > 1 else "Autor"
        author = f'{start}: {", ".join([str(a) for a in autorzy])}'
    else:
        author = "Autor nieznany"

    if song.kategorie:
        categories = list(song.kategorie.all())
        start = "Kategorie" if len(categories) > 1 else "Kategoria"
        category = f'{start}: {", ".join([str(c) for c in categories])}'
    else:
        category = "Brak kategorii"

    return render(
        request,
        "spiewnik/piosenka.html",
        {
            "text": formatted_lines,
            "title": song.tytul,
            "author": author,
            "category": category,
        },
    )
