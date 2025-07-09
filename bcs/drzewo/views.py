# drzewo/views.py
from django.http import FileResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .forms import *
import os
from drzewo.utils.draw_a_tree import generate_full_tree, generate_scoped_tree


@require_GET
def serve_full_tree_form_view(request):
    form = FullTreeRenderForm(request.GET)

    if form.is_bound and form.is_valid():
        onp = form.cleaned_data['only_known_parents']  # will be False if unchecked
        title = "full_tree"
        if onp:
            title += "_onp"

        path = f"/home/szymon/Desktop/bcs/bcs/drzewo/trees/{title}.png"

        if not os.path.exists(path):
            generate_full_tree(path, onp)

        if os.path.exists(path):
            return FileResponse(open(path, "rb"), content_type="image/png")

    return render(request, "drzewo/full_tree_generation.html", {"form": form})

@require_GET
def serve_scoped_tree_form_view(request):
    form = ScopedTreeRenderForm(request.GET or None)

    if form.is_valid():
        member = form.cleaned_data['member']
        depth = form.cleaned_data['depth']
        gen = form.cleaned_data['gen']

        title = f"tree_{member.id}_depth_{depth}_gen_{gen}"
        path = f"/home/szymon/Desktop/bcs/bcs/drzewo//trees/{title}.png"

        if not os.path.exists(path):
            generate_scoped_tree(path, member, depth, gen)

        if os.path.exists(path):
            return FileResponse(open(path, "rb"), content_type="image/png")

        raise Http404("Image not found after generation")

    return render(request, "drzewo/scoped_tree_generation.html", {"form": form})
