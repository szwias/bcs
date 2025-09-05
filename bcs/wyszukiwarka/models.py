import re
from django.db import models
from django.utils.html import escape, mark_safe
from wyszukiwarka.utils.Search import create_search_text


class SearchableModel(models.Model):
    search_text = models.TextField(editable=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.search_text = create_search_text(self)
        super().save(*args, **kwargs)

    import re
    from django.utils.html import escape, mark_safe

    def snippet(self, query, total_length=100):
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
