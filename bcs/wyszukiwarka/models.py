from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from polymorphic.models import PolymorphicModel


from wyszukiwarka.managers import (
    SearchableManager,
    SearchablePolymorphicManager,
)
from wyszukiwarka.utils.Search import find_searchable_fields


class AbstractSearchableModel(models.Model):
    search_dict = models.JSONField(
        editable=False, blank=True, null=True, default=dict
    )
    simple_tsv = SearchVectorField(null=True, editable=False)
    tsv = SearchVectorField(null=True, editable=False)

    LANGUAGE = "polish"

    class Meta:
        abstract = True

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
                continue
            elif isinstance(field, models.ManyToManyField):
                text_value = ", ".join(str(obj) for obj in value.all())
                if not text_value:
                    continue
            elif isinstance(field, ArrayField):
                text_value = ", ".join(str(el) for el in value)
                if not text_value:
                    continue
            else:
                text_value = str(value)

            pairs[field.name] = text_value

        return pairs


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
