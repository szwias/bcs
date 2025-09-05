from django.db import models

IGNORED_FIELD_NAMES = {"id"}
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


class SearchableModel(models.Model):
    search_text = models.TextField(editable=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.search_text = create_search_text(self)
        super().save(*args, **kwargs)

    def snippet(self, query, total_length=100):
        """
        Returns a snippet of the object's search_text containing the query,
        with the query roughly in the middle and total length limited.
        """
        if not self.search_text:
            return ""

        text = self.search_text
        query_lower = query.lower()
        index = text.lower().find(query_lower)

        if index == -1:
            # Query not found, just truncate start of text
            snippet = text[:total_length]
            return snippet + "..." if len(text) > total_length else snippet

        # Calculate snippet boundaries
        half_len = total_length // 2
        start = max(0, index - half_len)
        end = start + total_length

        # Adjust if end exceeds text length
        if end > len(text):
            end = len(text)
            start = max(0, end - total_length)

        snippet = text[start:end]

        # Add ellipses if snippet is not full text
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet
