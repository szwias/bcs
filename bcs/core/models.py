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
        if (
            field.name in IGNORED_FIELD_NAMES
            or field.name.endswith(IGNORED_FIELD_SUFFIXES)
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
