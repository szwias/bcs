import re

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models import Value
from django.utils.html import escape, mark_safe
from polymorphic.models import PolymorphicModel

from wyszukiwarka.managers import (
    SearchableManager,
    SearchablePolymorphicManager,
)
from wyszukiwarka.utils.Search import find_searchable_fields


class AbstractSearchableModel(models.Model):
    search_dict = models.JSONField(editable=False, blank=True, default=dict)

    tsv = SearchVectorField(null=True, editable=False)

    LANGUAGE = "polish"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.search_dict = self._create_search_dict()
        flattened_text = self._flatten_search_dict()
        self.tsv = SearchVector(Value(flattened_text), config=self.LANGUAGE)
        super().save(*args, **kwargs)

    def _flatten_search_dict(self):
        values = []
        for value in self.search_dict.values():
            if value != "":
                values.append(value)
        return " ".join(values)

    def _create_search_dict(self):
        pairs = {}
        for field in find_searchable_fields(self.__class__):
            # Assign choice display to value if field has choices
            if getattr(field, "choices", None):
                method = getattr(self, f"get_{field.name}_display", None)
                value = method() if method else None
            else:
                value = getattr(self, field.name, None)

            if not value:
                text_value = ""
            elif isinstance(field, models.ManyToManyField):
                text_value = ", ".join(str(obj) for obj in value.all())
            else:
                text_value = str(value)

            pairs[field.name] = text_value

        return pairs

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


class SearchableModel(AbstractSearchableModel):
    search_indexable = True

    objects = SearchableManager()

    class Meta:
        abstract = True


class SearchablePolymorphicModel(PolymorphicModel, AbstractSearchableModel):
    search_indexable = False

    objects = SearchablePolymorphicManager()

    class Meta:
        abstract = True
