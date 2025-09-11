# wyszukiwarka/managers.py
from django.db import models
from django.db.models import Value, F
from django.contrib.postgres.search import (
    SearchQuery,
    SearchHeadline,
    SearchRank,
)
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class SearchableQuerySet(models.QuerySet):
    def search_with_snippets(self, query_text, config="polish"):
        tsquery = SearchQuery(query_text, config=config)
        annotations = {}

        # Ranking based on precomputed tsvector
        if hasattr(self.model, "tsv"):
            annotations["rank"] = SearchRank(F("tsv"), tsquery)

        # For each instance, we want per-field snippets
        # We'll create annotations dynamically for all keys in search_dict
        if self.model._meta.get_field("search_dict"):
            # We can only annotate known keys at query time
            # So collect all possible keys in the model (or a representative set)
            example_obj = self.first()

            if not example_obj:
                return self.none()  # empty queryset

            for field_name in example_obj.search_dict.keys():
                annotations[f"{field_name}_snippet"] = SearchHeadline(
                    Value(example_obj.search_dict[field_name]),
                    tsquery,
                    start_sel="<span class='query-match'>",
                    stop_sel="</span>",
                    config=config,
                )

        return self.annotate(**annotations)


class SearchableManager(models.Manager):
    def get_queryset(self):
        return SearchableQuerySet(self.model, using=self._db)

    def search(self, query_text, config="polish"):
        return self.get_queryset().search_with_snippets(
            query_text, config=config
        )


class SearchablePolymorphicQuerySet(PolymorphicQuerySet):
    def search_with_snippets(self, query_text, config="polish"):
        tsquery = SearchQuery(query_text, config=config)
        annotations = {}

        # Ranking based on precomputed tsvector
        if hasattr(self.model, "tsv"):
            annotations["rank"] = SearchRank(F("tsv"), tsquery)

        # For each instance, we want per-field snippets
        # We'll create annotations dynamically for all keys in search_dict
        if self.model._meta.get_field("search_dict"):
            # We can only annotate known keys at query time
            # So collect all possible keys in the model (or a representative set)
            example_obj = self.first()

            if not example_obj:
                return self.none()  # empty queryset

            for field_name in example_obj.search_dict.keys():
                annotations[f"{field_name}_snippet"] = SearchHeadline(
                    Value(example_obj.search_dict[field_name]),
                    tsquery,
                    start_sel="<span class='query-match'>",
                    stop_sel="</span>",
                    config=config,
                )

        return self.annotate(**annotations)


class SearchablePolymorphicManager(PolymorphicManager):
    def get_queryset(self):
        return SearchablePolymorphicQuerySet(self.model, using=self._db)

    def search(self, query_text, config="polish"):
        # force non-polymorphic query, so annotations don’t break
        qs = self.get_queryset().non_polymorphic()
        return qs.search_with_snippets(query_text, config=config)
