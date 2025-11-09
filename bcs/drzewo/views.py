# drzewo/views.py
import os

from django.http import FileResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from drzewo.utils.draw_a_tree import generate_full_tree, generate_scoped_tree
from .forms import *

# TODO: add a view for choosing from full and scoped

accepting_strings = ("1", "true", "on", "True")


def parse_onp(request):
    return request.GET.get("only_known_parents") in accepting_strings


@require_GET
def serve_full_tree_form_view(request):
    form = FullTreeRenderForm(request.GET or None)

    # Only process if user actually submitted
    if "submitted" in request.GET and form.is_valid():
        onp = form.cleaned_data["only_known_parents"]

        title = "full_tree" + ("_onp" if onp else "")
        path = f"/home/szymon/Desktop/bcs/bcs/drzewo/trees/{title}.png"

        if not os.path.exists(path):
            generate_full_tree(path=path, onp=onp)

        if os.path.exists(path):
            return FileResponse(open(path, "rb"), content_type="image/png")

        raise Http404("Image not found after generation")

    return render(
        request=request,
        template_name="drzewo/full_tree_generation.html",
        context={"form": form},
    )


@require_GET
def full_tree_interactive_view(request):
    form = FullTreeRenderForm(request.GET or None)
    onp = parse_onp(request)
    print(onp)
    return render(
        request=request,
        template_name="drzewo/full_tree_interactive.html",
        context={"form": form, "onp": onp},
    )

@require_GET
def serve_scoped_tree_form_view(request):
    # TODO: add option of not showing first parent if there's a second one
    form = ScopedTreeRenderForm(request.GET)

    if form.is_valid():
        member = form.cleaned_data["member"]
        depth = form.cleaned_data["depth"]
        gen = form.cleaned_data["gen"]
        onp = form.cleaned_data["only_known_parents"]

        title = f"tree_{member.id}_depth_{depth}_gen_{gen}" + (
            "_onp" if onp else ""
        )
        path = f"/home/szymon/Desktop/bcs/bcs/drzewo//trees/{title}.png"

        if not os.path.exists(path):
            generate_scoped_tree(
                path=path, member=member, depth=depth, gen=gen, onp=onp
            )

        if os.path.exists(
            path
        ):  # TODO: generate anyway if related models' records changed
            return FileResponse(open(path, "rb"), content_type="image/png")

        raise Http404("Image not found after generation")

    return render(
        request=request,
        template_name="drzewo/scoped_tree_generation.html",
        context={"form": form},
    )
