import re

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import escape, mark_safe


class SearchableModel(models.Model):
    search_text = models.TextField(editable=False, blank=True)

    fields_positions = models.JSONField(
        editable=False, blank=True, default=list
    )

    IGNORED_FIELD_SUFFIXES = ("_ptr", "_ctype", "_id")
    IGNORED_FIELD_TYPES = (
        models.AutoField,
        models.FileField,
        models.ImageField,
        models.BooleanField,
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
        offset = start  # positions are relative to snippet

        # Step 2: Apply italics only to intersecting field names
        styled_positions = []
        for field_start, field_end in self.fields_positions or []:
            # Skip if outside snippet
            if field_end <= start or field_start >= end:
                continue
            # Clip to snippet bounds
            rel_start = max(0, field_start - offset)
            rel_end = min(end - start, field_end - offset)
            styled_positions.append((rel_start, rel_end))

        # Insert <span class="field-name"> tags in reverse order
        for s, e in reversed(styled_positions):
            snippet_text = snippet_text[:e] + "</span>" + snippet_text[e:]
            snippet_text = (
                snippet_text[:s]
                + '<span class="field-name">'
                + snippet_text[s:]
            )

        # Step 3: Highlight query after field-name spans
        snippet_text = re.sub(
            query_escaped,
            lambda m: f'<span class="query-match">{escape(m.group(0))}</span>',
            snippet_text,
            flags=re.IGNORECASE,
        )

        # Step 4: Add ellipses if needed
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
        positions = []
        current_index = 0

        for field in self._meta.get_fields():
            # Skip reverse relations
            if field.auto_created and not field.concrete:
                continue

            if field.name.endswith(self.IGNORED_FIELD_SUFFIXES):
                continue

            if hasattr(field, "editable") and not field.editable:
                continue

            if isinstance(field, self.IGNORED_FIELD_TYPES):
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
            name_end = (
                current_index + len(field.name) + 1
            )  # +1 for : character
            positions.append([name_start, name_end])

            # Update index (plus 1 for " ")
            current_index += len(piece) + 1

        return " ".join(properties), positions
