from PyPDF2 import PdfReader
from django.db import models

IGNORED_FIELD_NAMES = {"id", "search_text"}
IGNORED_FIELD_SUFFIXES = ("_ptr", "_ctype", "_id")
IGNORED_FIELD_TYPES = (
    models.AutoField,
    models.FileField,
    models.ImageField,
    models.BooleanField,
)


def create_search_text(instance):
    """
    Build a search_text string for a model instance by joining all relevant fields.
    """
    values = []

    for field in instance._meta.get_fields():
        # Skip reverse relations
        if field.auto_created and not field.concrete:
            continue

        # Skip ignored names or suffixes
        if field.name in IGNORED_FIELD_NAMES or field.name.endswith(
            IGNORED_FIELD_SUFFIXES
        ):
            continue

        # Skip fields by type
        if isinstance(field, IGNORED_FIELD_TYPES):
            continue

        try:
            value = getattr(instance, field.name, None)
        except Exception:
            # If field is problematic, skip it
            continue

        if value is None:
            continue

        # Handle ManyToMany
        if isinstance(field, models.ManyToManyField):
            values.extend(str(obj) for obj in value.all())
        else:
            values.append(str(value))

    return " ".join(values)


def extract_text_from_pdf(file_obj):
    """Extract text from a PDF file object."""
    file_obj.open("rb")  # Ensure file is open in binary mode
    reader = PdfReader(file_obj)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)
