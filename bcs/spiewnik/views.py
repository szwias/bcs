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
    lyrics = [line.get("tekst", "") for line in lines]
    chords = [" ".join(line.get("chwyty", [])) for line in lines]
    flags = [line.get("flag", "") for line in lines]

    # Determine fixed right alignment
    max_lyrics_len = max((len(l) for l in lyrics), default=0)
    max_chords_len = max((len(c) for c in chords), default=0)
    right_border = max_lyrics_len + 4 + max_chords_len

    is_bold = False
    is_highlighted = False

    for l, c, f in zip(lyrics, chords, flags):
        if not l and not c:
            formatted_lines.append("")  # blank line
            is_bold = False
            is_highlighted = False
            continue
        spaces_needed = right_border - len(l) - len(c)
        line_text = l + " " * spaces_needed + c

        # Determine if this line should be bold
        if l.strip() == "":
            is_bold = False
        else:
            if l.lower().startswith("ref") or l.lower().startswith("[ref"):
                is_highlighted = True
                is_bold = True
            elif is_bold or f == "refren":
                is_highlighted = False
                is_bold = True
            else:
                is_highlighted = False
                is_bold = False

        is_comment = f == "komentarz"

        formatted_lines.append(
            {
                "text": line_text,
                "bold": is_bold,
                "highlight": is_highlighted,
                "comment": is_comment
            }
        )

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
            "lines": formatted_lines,
            "title": song.tytul,
            "author": author,
            "category": category,
        },
    )
