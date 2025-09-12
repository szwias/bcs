# wyszukiwarka/managers.py
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.contrib.postgres.search import (
    SearchQuery,
    SearchHeadline,
    SearchRank,
)
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet

from core.utils.Misc import JsonExtractText
from wyszukiwarka.utils.Search import find_searchable_fields


class SearchableQuerySet(models.QuerySet):
    def search_with_snippets(self, query_text, config="polish"):
        tsquery = SearchQuery(query_text, config=config)
        annotations = {}

        if config != "simple" and hasattr(self.model, "tsv"):
            qs = self.filter(tsv=tsquery)
            annotations["rank"] = SearchRank(F("tsv"), tsquery)
        elif config == "simple" and hasattr(self.model, "simple_tsv"):
            qs = self.filter(simple_tsv=tsquery)
            annotations["rank"] = SearchRank(F("simple_tsv"), tsquery)
        else:
            qs = self

        # Field-specific snippets from search_dict
        if self.model._meta.get_field("search_dict"):
            for field in find_searchable_fields(self.model):
                annotations[f"{field.name}_snippet"] = SearchHeadline(
                    JsonExtractText(F("search_dict"), field.name),
                    tsquery,
                    start_sel="<span class='query-match'>",
                    stop_sel="</span>",
                    config=config,
                    max_words=40,  # total words in snippet
                    min_words=20,  # words around match
                )

        return qs.annotate(**annotations)


class SearchableManager(models.Manager):
    def get_queryset(self):
        return SearchableQuerySet(self.model, using=self._db)

    def search(self, query_text, config="polish"):
        return self.get_queryset().search_with_snippets(
            query_text, config=config
        )


class SearchablePolymorphicQuerySet(SearchableQuerySet, PolymorphicQuerySet):
    def search_with_snippets(self, query_text, config="polish"):

        if (
            hasattr(self.model, "polymorphic_base_model")
            and self.model == self.model.polymorphic_base_model
        ):
            return self

        return SearchableQuerySet.search_with_snippets(
            self, query_text, config
        )


class SearchablePolymorphicManager(PolymorphicManager):
    def get_queryset(self):
        return SearchablePolymorphicQuerySet(self.model, using=self._db)

    def search(self, query_text, config="polish"):
        # force non-polymorphic query, so annotations don’t break
        qs = self.get_queryset().non_polymorphic()

        # Only include instances of this exact model
        model_ct = ContentType.objects.get_for_model(self.model)
        qs = qs.filter(polymorphic_ctype=model_ct)

        return qs.search_with_snippets(query_text, config=config)
