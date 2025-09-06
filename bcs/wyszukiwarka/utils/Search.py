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
    Build a search_text string for a model instance and also record
    positions of field names for styling later.
    """
    properties = []
    positions = []
    current_index = 0

    for field in instance._meta.get_fields():
        # Skip reverse relations
        if field.auto_created and not field.concrete:
            continue

        if field.name in IGNORED_FIELD_NAMES or field.name.endswith(IGNORED_FIELD_SUFFIXES):
            continue

        if isinstance(field, IGNORED_FIELD_TYPES):
            continue

        # Resolve field value
        if getattr(field, "choices", None):
            method = getattr(instance, f"get_{field.name}_display", None)
            value = method() if method else ""
        else:
            value = getattr(instance, field.name, "")

        if not value:
            continue

        # Format "field: value"
        if isinstance(field, models.ManyToManyField):
            text_value = ", ".join(str(obj) for obj in value.all())
        else:
            text_value = str(value)

        piece = f"{field.name}: {text_value}"
        properties.append(piece)

        # Record the field name position (only the name itself)
        name_start = current_index
        name_end = current_index + len(field.name) + 1 # +1 for : character
        positions.append((name_start, name_end))

        # Update index (plus 2 for ", ")
        current_index += len(piece) + 2

    return " ".join(properties), positions



def extract_text_from_pdf(file_obj):
    """Extract text from a PDF file object."""
    file_obj.open("rb")  # Ensure file is open in binary mode
    reader = PdfReader(file_obj)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)
