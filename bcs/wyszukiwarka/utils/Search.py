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
