# spiewnik/views.py
import json

from django.contrib.admin.utils import quote
from django.shortcuts import render, get_object_or_404
from collections import defaultdict

from django.urls import reverse

from .models import Piosenka, KategoriaPiosenki


def spis_tresci(request):
    categories = KategoriaPiosenki.objects.all().order_by("nazwa")
    songs_by_category = []

    for category in categories:
        songs = Piosenka.objects.filter(kategorie=category).order_by("tytul")
        songs_by_category.append((category, songs))

    uncategorized = Piosenka.objects.filter(kategorie__isnull=True).order_by(
        "tytul"
    )

    return render(
        request,
        "spiewnik/spis_tresci.html",
        {
            "songs_by_category": songs_by_category,
            "uncategorized": uncategorized,
        },
    )


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
                "comment": is_comment,
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

    admin_url = reverse(
        f"admin:spiewnik_piosenka_change",
        args=(quote(song.pk),),
    )

    return render(
        request,
        "spiewnik/piosenka.html",
        {
            "lines": formatted_lines,
            "title": song.tytul,
            "author": author,
            "category": category,
            "admin_url": admin_url,
        },
    )
