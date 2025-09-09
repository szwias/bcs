import re

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.utils.html import escape, mark_safe

from wyszukiwarka.utils.Search import find_searchable_fields


class SearchableModel(models.Model):
    search_text = models.TextField(editable=False, blank=True)

    tsv = SearchVectorField(null=True, editable=False)

    IGNORED_FIELD_SUFFIXES = ("_ptr", "_ctype", "_id")
    IGNORED_FIELD_TYPES = (
        models.AutoField,
        models.FileField,
        models.ImageField,
        models.BooleanField,
    )
    LANGUAGE = "polish"

    class Meta:
        abstract = True
        indexes = [
            GinIndex(fields=["tsv"]),
        ]

    def save(self, *args, **kwargs):
        self.tsv = SearchVector("search_text", config=self.LANGUAGE)
        super().save(*args, **kwargs)

    def snippet(self, query, total_length=200):
        if not self.search_text:
            return ""

        text = self.search_text
        query_escaped = re.escape(query)
        match = re.search(query_escaped, text, flags=re.IGNORECASE)

        # Step 1: Determine snippet boundaries
        if match:
            start_idx, end_idx = match.start(), match.end()
            half_len = total_length // 2
            start = max(0, start_idx - half_len)
        else:
            start = 0
        end = min(len(text), start + total_length)

        snippet_text = text[start:end]

        # Step 2: Highlight query after field-name spans
        snippet_text = re.sub(
            query_escaped,
            lambda m: f'<span class="query-match">{escape(m.group(0))}</span>',
            snippet_text,
            flags=re.IGNORECASE,
        )

        # Step 3: Add ellipses if needed
        if start > 0:
            snippet_text = "..." + snippet_text
        if end < len(text):
            snippet_text += "..."

        return mark_safe(snippet_text)

    def _create_search_text(self):
        """
        Build search_text and record positions of field names for styling later.
        """
        properties = []
        current_index = 0

        for field in find_searchable_fields(self.__class__):

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

            # Update index (plus 1 for " ")
            current_index += len(piece) + 1

        return " ".join(properties)
