import re
from PyPDF2 import PdfReader

from django.db import models


def extract_text_from_pdf(file_obj):
    """Extract text from a PDF file object."""
    file_obj.open("rb")  # Ensure file is open in binary mode
    reader = PdfReader(file_obj)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)


IGNORED_FIELD_SUFFIXES = ("_ptr", "_ctype", "_id")
IGNORED_FIELD_TYPES = (
    models.AutoField,
    models.FileField,
    models.ImageField,
    models.BooleanField,
    models.URLField,
)


def find_searchable_fields(model):
    searchable_fields = []
    for field in model._meta.get_fields():
        if field.auto_created and not field.concrete:
            continue

        if field.name.endswith(IGNORED_FIELD_SUFFIXES):
            continue

        if isinstance(field, IGNORED_FIELD_TYPES):
            continue

        if hasattr(field, "editable") and not field.editable:
            continue

        searchable_fields.append(field)

    return searchable_fields


def adjust_snippet_classes(snippet_html, query_text):
    pattern = r"<span class='search__query-match'>(.*?)</span>"

    def replacer(match):
        text = match.group(1)
        if text.lower() != query_text.lower():
            return f"<span class='search__near-match'>{text}</span>"
        return match.group(0)

    return re.sub(pattern=pattern, repl=replacer, string=snippet_html)


def add_ellipses(fragment, full_text):
    """
    Adds ellipses at the start/end if fragment is truncated from the full text.
    Handles <span class='query-match'> tags correctly.
    """
    # Remove query highlight tags
    real_fragment = re.sub(
        pattern=r"<span class=['\"]search__query-match['\"]>",
        repl="",
        string=fragment,
    )
    real_fragment = real_fragment.replace("</span>", "")

    start = full_text.find(real_fragment)
    end = start + len(real_fragment) if start >= 0 else -1

    adjusted_fragment = fragment
    if start > 0:
        adjusted_fragment = "… " + adjusted_fragment
    if end != -1 and end < len(full_text):
        adjusted_fragment = adjusted_fragment + " …"

    return adjusted_fragment
