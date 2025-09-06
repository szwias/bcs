import re

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import escape, mark_safe

IGNORED_FIELD_NAMES = {"id", "search_text"}
IGNORED_FIELD_SUFFIXES = ("_ptr", "_ctype", "_id")
IGNORED_FIELD_TYPES = (
    models.AutoField,
    models.FileField,
    models.ImageField,
    models.BooleanField,
)


class SearchableModel(models.Model):
    search_text = models.TextField(editable=False, blank=True)

    fields_positions = models.JSONField(
        editable=False, blank=True, default=list
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        text, positions = self._create_search_text()
        self.search_text = text
        self.fields_positions = positions
        super().save(*args, **kwargs)

    def snippet(self, query, total_length=200):
        if not self.search_text:
            return ""

        text = self.search_text
        match = re.search(re.escape(query), text, flags=re.IGNORECASE)

        if not match:
            start, end = 0, min(len(text), total_length)
        else:
            start_idx, end_idx = match.start(), match.end()
            half_len = total_length // 2
            start = max(0, start_idx - half_len)
            end = min(len(text), start + total_length)

        snippet_text = text[start:end]
        offset = start

        # --- Step 1: Apply italics for field names ---
        for pos_start, pos_end in reversed(self.fields_positions or []):
            if pos_end < start or pos_start > end:
                continue
            rel_start = max(0, pos_start - offset)
            rel_end = min(len(snippet_text), pos_end - offset)
            snippet_text = snippet_text[:rel_end] + "</em>" + snippet_text[
                                                              rel_end:]
            snippet_text = snippet_text[:rel_start] + "<em>" + snippet_text[
                                                               rel_start:]

        # --- Step 2: Highlight query after italics ---
        query_escaped = re.escape(query)
        snippet_text = re.sub(
            query_escaped,
            lambda m: f"<strong>{escape(m.group(0))}</strong>",
            snippet_text,
            flags=re.IGNORECASE,
        )

        # Add ellipses if needed
        if start > 0:
            snippet_text = "..." + snippet_text
        if end < len(text):
            snippet_text += "..."

        return mark_safe(snippet_text)

    def title(self):
        model_class = ContentType.objects.get_for_model(self).model_class()
        return f"{model_class.__name__}: {str(self)}"

    def _create_search_text(self):
        """
        Build search_text and record positions of field names for styling later.
        """
        properties = []
        positions = []
        current_index = 0

        for field in self._meta.get_fields():
            # Skip reverse relations
            if field.auto_created and not field.concrete:
                continue

            if field.name in IGNORED_FIELD_NAMES or field.name.endswith(
                    IGNORED_FIELD_SUFFIXES):
                continue

            if isinstance(field, IGNORED_FIELD_TYPES):
                continue

            # Resolve field value
            if getattr(field, "choices", None):
                method = getattr(self, f"get_{field.name}_display", None)
                value = method() if method else ""
            else:
                value = getattr(self, field.name, "")

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
            name_end = current_index + len(
                field.name) + 1  # +1 for : character
            positions.append([name_start, name_end])

            # Update index (plus 2 for ", ")
            current_index += len(piece) + 2

        return " ".join(properties), positions
