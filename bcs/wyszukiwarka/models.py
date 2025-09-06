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
        """
        Returns a snippet of search_text with the query centered and bolded.
        """
        if not self.search_text:
            return ""

        text = self.search_text
        query_escaped = re.escape(query)
        match = re.search(query_escaped, text, flags=re.IGNORECASE)

        if not match:
            snippet = text[:total_length]
            if len(text) > total_length:
                snippet += "..."
            return escape(snippet)

        start_idx, end_idx = match.start(), match.end()
        half_len = total_length // 2

        start = max(0, start_idx - half_len)
        end = min(len(text), start + total_length)

        snippet = text[start:end]

        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        # Bold all occurrences of query
        snippet = re.sub(
            query_escaped,
            lambda m: f"<strong>{escape(m.group(0))}</strong>",
            snippet,
            flags=re.IGNORECASE,
        )

        return mark_safe(snippet)

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
            positions.append((name_start, name_end))

            # Update index (plus 2 for ", ")
            current_index += len(piece) + 2

        return " ".join(properties), positions

    def title(self):
        model_class = ContentType.objects.get_for_model(self).model_class()
        return f"{model_class.__name__}: {str(self)}"
