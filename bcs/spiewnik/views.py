# spiewnik/views.py
import json
from unicodedata import category

from django.contrib.admin.utils import quote
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Piosenka, KategoriaPiosenki


def spis_tresci(request):
    categories = KategoriaPiosenki.objects.all().order_by("nazwa")
    songs_by_category = []

    for category in categories:
        songs = Piosenka.objects.filter(kategorie=category).order_by("tytul")
        if songs:
            songs_by_category.append((category, songs))

    uncategorized = Piosenka.objects.filter(kategorie__isnull=True).order_by(
        "tytul"
    )

    return render(
        request=request,
        template_name="spiewnik/spis_tresci.html",
        context={
            "songs_by_category": songs_by_category,
            "uncategorized": uncategorized,
        },
    )


def spis_tresci_kat(request, category_pk):
    category = KategoriaPiosenki.objects.get(pk=category_pk)
    songs = list(
        Piosenka.objects.filter(kategorie__pk=category_pk).order_by("tytul")
    )
    print(songs)

    return render(
        request=request,
        template_name="spiewnik/spis_tresci_kat.html",
        context={"category": category, "songs": songs},
    )


def piosenka(request, category_pk, pk):
    song = Piosenka.objects.get(pk=pk)
    song_category = None
    songs_in_category = []

    if category_pk:
        song_category = get_object_or_404(KategoriaPiosenki, pk=category_pk)
        songs_in_category = list(
            Piosenka.objects.filter(kategorie=song_category).order_by("tytul")
        )

    # get index of the current song in the category
    try:
        index = next(
            i for i, s in enumerate(songs_in_category) if s.pk == song.pk
        )
    except StopIteration:
        index = None

    prev_song = songs_in_category[index - 1] if index and index > 0 else None
    next_song = (
        songs_in_category[index + 1]
        if index is not None and index < len(songs_in_category) - 1
        else None
    )

    lines = []
    if song.tekst:
        with song.tekst.open("r") as f:
            lines = json.load(f)

    text_col_width = max(
        (len(line.get("tekst", "")) for line in lines), default=40
    )
    chords_col_width = max(
        (len(" ".join(line.get("chwyty", []))) for line in lines), default=0
    )

    formatted_lines = []
    is_bold = False

    for line in lines:
        l = line.get("tekst", "")
        chords_list = line.get("chwyty", [])
        flaga = line.get("flaga", "")

        # Determine if bold/highlight
        is_highlighted = False
        if l.strip():
            if l.lower().startswith("ref") or l.lower().startswith("[ref"):
                is_bold = True
                is_highlighted = True
            elif is_bold or flaga == "refren":
                is_bold = True
        elif flaga == "refren":
            is_bold = True
        else:
            is_bold = False

        is_comment = flaga == "komentarz"

        formatted_lines.append(
            {
                "text": l,
                "chords": chords_list,
                "bold": is_bold,
                "highlight": is_highlighted,
                "comment": is_comment,
            }
        )

    # Author
    if song.autor:
        author = f"Autor: {song.autor}"
    elif song.znani_czapce_autorzy.exists():
        autorzy = list(song.znani_czapce_autorzy.all())
        start = "Autorzy" if len(autorzy) > 1 else "Autor"
        author = f'{start}: {", ".join([str(a) for a in autorzy])}'
    else:
        author = "Autor nieznany"

    # Category
    if song.kategorie.exists():
        categories = list(song.kategorie.all())
    else:
        categories = []

    # Admin URL
    admin_url = reverse(
        "admin:spiewnik_piosenka_change", args=(quote(song.pk),)
    )

    return render(
        request=request,
        template_name="spiewnik/piosenka.html",
        context={
            "lines": formatted_lines,
            "title": song.tytul,
            "author": author,
            "categories": categories,
            "category": song_category,
            "prev_song": prev_song,
            "next_song": next_song,
            "admin_url": admin_url,
            "text_col_width": text_col_width + 4,
            "chords_col_width": chords_col_width,
        },
    )
